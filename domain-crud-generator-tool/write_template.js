const fs = require('fs');
const path = require('path');
const Handlebars = require('handlebars');

/**
 * Reads a Handlebars template, compiles it with data, and writes to output file
 * @param {string} templateFile - The template file name (in template directory)
 * @param {string} outputPath - The output file path
 * @param {object} data - The data to pass to the template
 */
function writeTemplate(templateFile, outputPath, data) {
  const templatePath = path.join(__dirname, 'template', templateFile);
  
  // Read template file
  const templateSource = fs.readFileSync(templatePath, 'utf-8');
  
  // Compile template
  const template = Handlebars.compile(templateSource);
  
  // Generate content
  const content = template(data);
  
  // Write to output file
  fs.writeFileSync(outputPath, content, 'utf-8');
}

module.exports = writeTemplate;
