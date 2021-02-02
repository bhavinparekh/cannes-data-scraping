# Cannes Data Scraping

This project allow the transformation of scraped data to an importable JSON file on the backoffice.clicknlerins.fr

---

## Requirement

For development, you will only need Node.js and a node global package, Yarn, installed in your environement.

### Node

- #### Node installation on Windows

  Just go on [official Node.js website](https://nodejs.org/) and download the installer.
  Also, be sure to have `git` available in your PATH, `npm` might need it (You can find git [here](https://git-scm.com/)).

- #### Node installation on Ubuntu

  You can install nodejs and npm easily with NVM.

- ##### Install NVM

  ```bash
    # Install NVM
    curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.37.2/install.sh | bash

    # Reload your ~/.bashrc
    source ~/.bashrc
  ```

- ##### Install Node 15

  ```bash
    # Install Node
    nvm install 15

    # Set default version of node
    nvm alias default 15
  ```

- #### Other Operating Systems
  You can find more information about the installation on the [official Node.js website](https://nodejs.org/) and the [official NPM website](https://npmjs.org/).

If the installation was successful, you should be able to run the following command.

```bash
  node --version
  # v15.3.0

  npm --version
  #7.0.14
```

###

### Yarn installation

After installing node, this project will need yarn too, so just run the following command.

```bash
curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -
echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list

# Since we did install node js with NVM we have to use this command to install Yarn
sudo apt update && sudo apt install --no-install-recommends yarn

# Add yarn to your path for the global packages
# Add this line at the end of your
export PATH="$PATH:`yarn global bin`" ~/.bashrc

# Reload your ~/.bashrc
source ~/.bashrc

```

---

## Install

```bash
  git clone git@gitlab.pertimm.net:klea/cannes-data-scraping.git
  cd cannes-data-scraping
  yarn install
```

## Running the script

```bash
  yarn start
```

## Steps to follow

- After you scrape a website, you add the resulted \*.json file in the `stores` directory
- You import that file in the main.js file
  - Example import VARIABLE_NAME from "../stores/JSON_FILE_NAME"; // STORE UID to get from the backoffice
- Call the function `generateFlux` on that file
  - Example
  ```javascript
  await generateFlux(
    VARIABLE_NAME,
    "FILE_EXPORT_NAME",
    "STORE UID",
    "UNIVERSE_NAME"
  );
  ```
  - The UNIVERSE_NAME must be choosen from on of the created in the backoffice (https://backoffice.clicknlerins.fr/#/universes)
- The generated files will be under the workspace dir ( check the `workspaceDir` variable in the file `src/functions.js`)

Check the `src/main.js` file form more understanding
