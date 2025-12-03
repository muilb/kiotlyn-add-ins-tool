const fs = require('fs');
const path = require('path');

/**
 * Recursively creates directory structure
 * @param {string} dirPath - The directory path to create
 */
function makedir(dirPath) {
  if (!fs.existsSync(dirPath)) {
    fs.mkdirSync(dirPath, { recursive: true });
    console.log(`Created directory: ${dirPath}`);
  }
}

module.exports = makedir;
