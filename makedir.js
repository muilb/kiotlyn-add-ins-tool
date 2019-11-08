/** make dir if not exit */

/** desDir get from argv 2 */
// console.log('test args env', process.env.args, process.argv);
const fs = require('fs');
function mkDir(path) {
    // check if exit
    if (!fs.existsSync(path)) {
        fs.mkdirSync(path);
        return path;
    } else {
        return {
            error: 'Is exist'
        }
    }
}
module.exports = mkDir;