const fs = require('fs');
const path = require('path');
const { parse } = require('csv-parse/sync');

// Get command line arguments
const args = process.argv.slice(2);

if (args.length < 2) {
  console.log('Usage: node index.js <csvFile> <outputFile>');
  console.log('Example: node index.js columns.csv EntityFields.java');
  console.log('');
  console.log('CSV Format: Tên gợi nhớ;columnname;datatype(length);NotNull');
  console.log('Example CSV:');
  console.log('Mã văn bản;ACV_TXT_CODE;VARCHAR(50);Yes');
  console.log('Tên tùy chọn;OPTIONAL_NAME;VARCHAR(100);');
  console.log('ID chính;PRIMARY_ID;BIGINT;Yes(PK)');
  console.log('Ngày tạo;CREATED_DATE;TIMESTAMP;Yes');
  console.log('Số trang;PAGE_COUNT;INT;');
  process.exit(1);
}

const csvFile = args[0];
const outputFile = args[1];

// Check if CSV file exists
if (!fs.existsSync(csvFile)) {
  console.error(`Error: CSV file not found: ${csvFile}`);
  process.exit(1);
}

/**
 * Convert UPPER_SNAKE_CASE to camelCase
 * @param {string} str - The string to convert
 * @returns {string} The converted string
 */
function toCamelCase(str) {
  return str.toLowerCase().replace(/_([a-z])/g, (_, letter) => letter.toUpperCase());
}

/**
 * Map SQL datatype to Java datatype
 * @param {string} sqlType - SQL datatype (e.g., VARCHAR, INT, TIMESTAMP)
 * @returns {string} Java datatype
 */
function mapDataType(sqlType) {
  const type = sqlType.toUpperCase();
  
  if (type.startsWith('VARCHAR') || type.startsWith('CHAR') || type.startsWith('TEXT') || type.startsWith('NVARCHAR')) {
    return 'String';
  } else if (type === 'INT' || type === 'INTEGER' || type === 'SMALLINT') {
    return 'Integer';
  } else if (type === 'BIGINT' || type === 'LONG') {
    return 'Long';
  } else if (type.startsWith('DECIMAL') || type.startsWith('NUMERIC') || type.startsWith('NUMBER')) {
    return 'BigDecimal';
  } else if (type === 'DATE') {
    return 'LocalDate';
  } else if (type === 'TIMESTAMP' || type === 'DATETIME') {
    return 'LocalDateTime';
  } else if (type === 'TIME') {
    return 'LocalTime';
  } else if (type === 'BOOLEAN' || type === 'BOOL' || type === 'BIT') {
    return 'Boolean';
  } else if (type === 'FLOAT' || type === 'REAL') {
    return 'Float';
  } else if (type === 'DOUBLE') {
    return 'Double';
  } else if (type.startsWith('BLOB') || type.startsWith('BINARY')) {
    return 'byte[]';
  } else {
    return 'String'; // Default to String for unknown types
  }
}

/**
 * Parse datatype to extract type and length
 * @param {string} datatype - Datatype string (e.g., VARCHAR(50), INT)
 * @returns {object} Object with type and length
 */
function parseDataType(datatype) {
  const match = datatype.match(/^([A-Z]+)(?:\((\d+)\))?/i);
  if (match) {
    return {
      type: match[1],
      length: match[2] || null
    };
  }
  return {
    type: datatype,
    length: null
  };
}

/**
 * Generate Java field with annotation
 * @param {string} comment - Field comment (Tên gợi nhớ)
 * @param {string} columnName - Database column name
 * @param {string} datatype - SQL datatype
 * @param {string} notNull - NotNull indicator (Yes, Yes(PK), or empty)
 * @returns {string} Generated Java field code
 */
function generateField(comment, columnName, datatype, notNull = '') {
  const fieldName = toCamelCase(columnName);
  const { type, length } = parseDataType(datatype);
  const javaType = mapDataType(type);
  
  // Determine if field is nullable
  const isNotNull = notNull && (notNull.trim().toUpperCase() === 'YES' || notNull.trim().toUpperCase().startsWith('YES('));
  
  let field = `  // ${comment}\n`;
  
  // Build @Column annotation
  let columnAnnotation = `  @Column(name = "${columnName}"`;
  
  // Add length for String types
  if (javaType === 'String' && length) {
    columnAnnotation += `, length = ${length}`;
  }
  
  // Add nullable parameter
  if (isNotNull) {
    columnAnnotation += ', nullable = false';
  }
  
  columnAnnotation += ')';
  
  field += columnAnnotation + '\n';
  field += `  private ${javaType} ${fieldName};\n`;
  
  return field;
}

try {
  // Read CSV file
  const csvContent = fs.readFileSync(csvFile, 'utf-8');
  
  // Parse CSV
  const records = parse(csvContent, {
    delimiter: ';',
    skip_empty_lines: true,
    trim: true
  });
  
  if (records.length === 0) {
    console.error('Error: CSV file is empty');
    process.exit(1);
  }
  
  console.log(`Processing ${records.length} columns...`);
  
  // Generate fields
  const fields = [];
  const imports = new Set(['jakarta.persistence.Column']);
  
  records.forEach((record, index) => {
    if (record.length < 3) {
      console.warn(`Warning: Line ${index + 1} has insufficient data, skipping...`);
      return;
    }
    
    const [comment, columnName, datatype, notNull = ''] = record;
    const field = generateField(comment.trim(), columnName.trim(), datatype.trim(), notNull.trim());
    fields.push(field);
    
    // Add imports based on datatype
    const { type } = parseDataType(datatype);
    const javaType = mapDataType(type);
    
    if (javaType === 'BigDecimal') {
      imports.add('java.math.BigDecimal');
    } else if (javaType === 'LocalDate') {
      imports.add('java.time.LocalDate');
    } else if (javaType === 'LocalDateTime') {
      imports.add('java.time.LocalDateTime');
    } else if (javaType === 'LocalTime') {
      imports.add('java.time.LocalTime');
    }
  });
  
  // Generate output
  let output = '// Generated Entity Fields\n';
  output += '// Date: ' + new Date().toISOString() + '\n\n';
  
  // Add imports
  output += '// Required imports:\n';
  imports.forEach(imp => {
    output += `// import ${imp};\n`;
  });
  output += '\n';
  
  // Add fields
  output += fields.join('\n');
  
  // Write to output file
  fs.writeFileSync(outputFile, output, 'utf-8');
  
  console.log('\n========================================');
  console.log(`Successfully generated ${fields.length} fields!`);
  console.log('========================================');
  console.log(`Output file: ${path.resolve(outputFile)}`);
  console.log('\nRequired imports:');
  imports.forEach(imp => console.log(`  import ${imp};`));
  
} catch (error) {
  console.error('Error:', error.message);
  process.exit(1);
}
