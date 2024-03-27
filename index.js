const fs = require("fs").promises;
const path = require("path");

const base_path = "./old_docs";
const updated_docs_base_path = "./new_docs";

const toTransform = [];
const categoryData = [];
const missingData = [];

const checkIfDir = async (fos) => {
  const fileStat = await fs.lstat(fos);
  return fileStat.isDirectory();
};

const getDirsToTransform = async (dir) => {
  const fileSystemObjects = await fs.readdir(dir);
  if (dir.includes("\\ar\\")) console.log("Checking:\n", fileSystemObjects);
  for (const fos of fileSystemObjects) {
    const isDir = await checkIfDir(path.join(dir, fos));

    if (!isDir) {
      if (fos.includes("missing.json")) {
        missingData.push(path.join(dir, fos));
      }

      if (fos.includes("current.json")) {
        missingData.push(path.join(dir, fos));
      }
    } else if (isDir) {
      const subFiles = await fs.readdir(path.join(dir, fos));
      if (dir.includes("\\ar\\")) console.log("FOS:\n", dir, fos, subFiles);

      if (subFiles.includes("page.mdx")) {
        toTransform.push(path.join(dir, fos, "page.mdx"));
      }

      if (subFiles.includes("_category_.json")) {
        categoryData.push(path.join(dir, fos, "_category_.json"));
      }

      await getDirsToTransform(path.join(dir, fos));
    } else {
      return;
    }
  }
  return;
};

const ensureDirectoryExists = async (dirPath) => {
  try {
    // console.log("checking if dir:", dirPath, "Exists");
    await fs.access(dirPath);
  } catch (error) {
    // Directory doesn't exist, so create it
    await fs.mkdir(dirPath, { recursive: true });
  }
};

// const transformIframe = (page) => {
//   let importAdded = false;

//   return page.replace(
//     /<iframe[\r\n\s]*src="https:\/\/embed\.learnprompting\.org\/embed\?config=(.*)"[\r\n\s]*style={({[\s\r\n\w:"%,]*})}[\r\n\s]*.*[\r\n\s]*><\/iframe>/gm,
//     function (matched, $0, $1) {
//       // console.log("matched", matched);
//       const decodedURL = decodeUrlConfig($0);
//       const model = decodedURL["model"];

//       if (!VALID_MODELS.includes(model)) {
//         decodedURL["model"] = "gpt-3.5-turbo";
//       }

//       const fixedStyles = JSON.parse(
//         $1
//           .replace(/[\n\r]/g, "")
//           .replace(/,\s*}/g, "}")
//           .replace(/(\w*):/g, '"$1":')
//       );

//       fixedStyles["background"] = "#1f2937";
//       fixedStyles["padding"] = "2px";
//       const encodedURL = encodeUrlConfig(decodedURL);
//       // decodedURL["style"] = fixedStyles;

//       // const props = Object.entries(decodedURL).reduce(
//       //   (acc, curr) => acc + `${curr[0]} = {${JSON.stringify(curr[1])}} `,
//       //   ""
//       // );
//       // console.log("replacement:\n", replacement);
//       // let replacement = `<PlaygroundEmbed ${props} />`;

//       // importAdded
//       //   ? replacement
//       //   : (importAdded =
//       //       true &&
//       //       (replacement =
//       //         'import PlaygroundEmbed from "@/components/PlaygroundEmbed"\n\n' +
//       //         replacement));

//       replacement = `<iframe src="https://embed.learnprompting.org/embed?config=${encodedURL}"\nstyle={${JSON.stringify(
//         fixedStyles
//       )}}\nsandbox="allow-forms allow-modals allow-popups allow-presentation allow-same-origin allow-scripts"><\/iframe>`;

//       return replacement;
//     }
//   );
// };

// TODO: IMPLEMENT THIS
// Find a way to check if already has an alt tag
// If not, pull image name from src attribute
// And use that as alt tag

//SHOULD WORK BY USING REGEX TO FIND SRC AND USING THE LAST PATH FOR THE ALT
function transformImages(page) {
  return page.replace(/<Image([\s\S]*?)\/>/g, (match, matchGroupOne) => {
    console.log(page);
    console.log("===================================\nMatch Found!");
    console.log("match:\n", match);
    console.log("groupOne:\n", matchGroupOne);

    //REGEX TO FIND SRC AND ALT TAGS
    const srcRegex = /src={?["']([^"']*)["']}?/;
    const altRegex = /alt="([^"]*)"/;
    const srcMatch = matchGroupOne.match(srcRegex);
    const altMatch = matchGroupOne.match(altRegex);

    //GETS THE SRC ATTRIBUTE AND SPLITS IT TO GET THE IMAGE NAME
    if (srcMatch) {
      const src = srcMatch[1];
      const parts = src.split("/");
      const imageName = parts[parts.length - 1];
      const alt = imageName.split(".")[0].replace(/_/g, " ");

      //IF ALT TAG DOESN'T EXIST, ADD IT ELSE DO NOTHING
      if (!altMatch) {
        return match.replace(/\/>/, ` alt="${alt}" />`);
      } else {
        return match;
      }
    }
  });
}

const transformDocs = async () => {
  // Copy over all mdx files
  for (const file of toTransform) {
    //Page contains all the text from a given *.mdx file
    let page = await fs.readFile(file, "utf8");

    // ADD TRANSFORMATIONS TO PAGE FILES HERE
    // page = transformIframe(page);
    page = transformImages(page);

    const newFile = path.join(
      updated_docs_base_path,
      file.split("\\").slice([1]).join("/")
    );

    await ensureDirectoryExists(path.dirname(newFile));
    await fs.writeFile(path.join(newFile), page);
  }

  //Copy over all _category_.json
  for (const categoryFile of categoryData) {
    const split_path = categoryFile.split("\\").slice(1);
    const new_path = path.join(updated_docs_base_path, split_path.join("/"));

    await ensureDirectoryExists(path.dirname(new_path));
    await fs.copyFile(categoryFile, new_path);
  }

  // Copy over all missing.json
  for (const missingFile of missingData) {
    const split_path = missingFile.split("\\").slice(1);
    const new_path = path.join(updated_docs_base_path, split_path.join("/"));

    await ensureDirectoryExists(path.dirname(new_path));
    await fs.copyFile(missingFile, new_path);
  }
};

(async () => {
  await getDirsToTransform(base_path);
  await transformDocs();
})();
