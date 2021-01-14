import fs from "fs-extra";
import os from "os";
import path from "path";
import sha1 from "sha1";

// Directory to export the enriched stores
export const workspaceDir = path.join(os.tmpdir(), "/cannes/");
fs.ensureDirSync(workspaceDir, { mode: 0o777 });

console.log("You workspace dir is *", workspaceDir, "*");

/**
 *
 * @param {*} json  The imported JSON file
 * @param {*} fileName The name of the enriched file
 * @param {*} uid The id of the store to get from the Backoffice
 * @param {*} universe The universe name associated to the data ( To choose on from the liste on the Backoffice )
 */
export const generateFlux = async (json, fileName, uid, universe) => {
  const flux = [];
  for (let i = 0; i < json.length; i++) {
    const x = json[i];

    let picture = "https://clicknlerins.fr/s/mainApp/image/no-visual.png";
    if (Array.isArray(x.images)) {
      if (x.images[0]) {
        picture = x.images[0].replace(/^\/\//, "https://");
      }
    } else if (x.images) {
      picture = x.images.replace(/^\/\//, "https://");
    }

    if (x) {
      let price = x.price || null;
      if (price) {
        const regex = /(\d)\s+(?=\d)/g;
        const str = price.toString();
        const subst = `$1`;

        price = str.replace(regex, subst);

        price = parseFloat((price || "0.0").replace(",", "."));
      }
      if (price) {
        const newData = {
          id: sha1(x.url),
          title: x.title,
          description: x.description || "",
          image: picture,
          url_visuel_principal: picture,
          categories: (x.categories || []).map((x) => x.trim()),
          navigation: [],
          magasins: [
            {
              uid,
              prix: price,
              stock: 1,
              ventes_30: 0,
              published: true,
            },
          ],
        };

        if (newData.categories?.length > 0) {
          const values = newData.categories;
          const finalNavigation = [];

          for (let l = 0; l < values.length; l++) {
            const value = values[l];
            if (l === 0) {
              finalNavigation.push(`${universe}|${value}`);
            } else {
              finalNavigation.push(`${finalNavigation[l - 1]}|${value}`);
            }
          }
          newData.navigation = finalNavigation;
        }

        if (newData.navigation.length === 0) {
          newData.navigation.push(universe);
        }

        // Check if we already have an object with the same id
        const indexSame = flux.findIndex((t) => t.id === newData.id);
        if (indexSame !== -1) {
          flux[indexSame].navigation.push(...newData.navigation);
        } else {
          delete newData.categories;
          flux.push(newData);
        }
      }
    }
  }

  await fs.writeFile(
    path.join(workspaceDir, fileName),
    JSON.stringify(flux, null, 2)
  );
};
