const fs = require('fs');
const path = require('path');
const Handlebars = require('handlebars');
const makedir = require('./makedir');
const writeTemplate = require('./write_template');

// Get command line arguments
const args = process.argv.slice(2);

if (args.length < 3) {
  console.log('Usage: node index.js <EntityName> <basePackage> <basePath>');
  console.log('Example: node index.js Product jp.brycen.domain D:\\Work\\Projects\\pubdis-spring-baseline\\src\\main\\java');
  process.exit(1);
}

const entityName = args[0]; // e.g., "Product"
const basePackage = args[1]; // e.g., "jp.brycen.domain"
const basePath = args[2]; // e.g., "D:\Work\Projects\pubdis-spring-baseline\src\main\java"

// Generate variations of entity name
const entityNameLower = entityName.toLowerCase(); // e.g., "product"
const entityNameCamel = entityName.charAt(0).toLowerCase() + entityName.slice(1); // e.g., "product"

// Convert package to path
const packagePath = basePackage.replace(/\./g, path.sep); // e.g., "jp\brycen\domain"

// Create base directory
const domainBasePath = path.join(basePath, packagePath, entityNameLower);

// Define directory structure
const directories = [
  path.join(domainBasePath, 'controller'),
  path.join(domainBasePath, 'dto'),
  path.join(domainBasePath, 'entity'),
  path.join(domainBasePath, 'repository'),
  path.join(domainBasePath, 'service'),
  path.join(domainBasePath, 'service', 'implementation')
];

// Create all directories
directories.forEach(dir => {
  makedir(dir);
});

// Template data
const templateData = {
  entityName,
  entityNameLower,
  entityNameCamel,
  basePackage,
  packagePath: packagePath.replace(/\\/g, '.')
};

// Define files to generate
const filesToGenerate = [
  { template: 'Entity.txt', output: path.join(domainBasePath, 'entity', `${entityName}.java`) },
  { template: 'Repository.txt', output: path.join(domainBasePath, 'repository', `${entityName}Repository.java`) },
  { template: 'Service.txt', output: path.join(domainBasePath, 'service', `${entityName}Service.java`) },
  { template: 'ServiceImpl.txt', output: path.join(domainBasePath, 'service', 'implementation', `${entityName}ServiceImpl.java`) },
  { template: 'Dto.txt', output: path.join(domainBasePath, 'dto', `${entityName}Dto.java`) },
  { template: 'Controller.txt', output: path.join(domainBasePath, 'controller', `${entityName}Controller.java`) }
];

// Generate all files
let successCount = 0;
let failCount = 0;

filesToGenerate.forEach(file => {
  try {
    writeTemplate(file.template, file.output, templateData);
    console.log(`✓ Created: ${file.output}`);
    successCount++;
  } catch (error) {
    console.error(`✗ Failed to create ${file.output}:`, error.message);
    failCount++;
  }
});

console.log('\n========================================');
console.log(`Domain generation completed!`);
console.log(`Success: ${successCount} files`);
console.log(`Failed: ${failCount} files`);
console.log('========================================');
console.log(`\nGenerated domain structure at:`);
console.log(domainBasePath);
