const fs = require('fs');
const Handlebars = require('handlebars');

/** write file from tempate file with text 
 * @param filename full path save file
 * @param template temp file path
 * @param tmptext json with repli text 
*/
function writeFile(filename, template, tmptext) {
    var tmp = fs.readFileSync(template, 'utf8');
    var compile = Handlebars.compile(tmp.toString());
    const contents = compile(tmptext);
    fs.writeFile(filename, contents, err => {
        if (err) {
            return console.error(`Autsch! Failed to store template: ${err.message}.`);
        }
        console.log('Saved template!', filename);
    });
}

module.exports = writeFile;

