# Domain CRUD Generator Tool

A Node.js tool for automatically generating Spring Boot CRUD domain structures with Entity, Repository, Service, Controller, and DTO using only Lombok without MapStruct dependency.

## Features

- **Simple CRUD Pattern**: Generates standard CRUD operations with complete implementation
- **Lombok-Based**: Uses only Lombok annotations, no MapStruct required
- **DTO Conversion Methods**: Includes `toEntity()` and `fromEntity()` methods in DTO
- **Standard Structure**: Creates 6 files (Entity, Repository, Service interface, ServiceImpl, DTO, Controller)
- **Validation Ready**: Includes Jakarta validation annotations
- **REST API Ready**: Automatically generates REST endpoints with `/api/v1/{entity}` path
- **Full CRUD Implementation**: Complete service interface and implementation without inheritance

## Prerequisites

- Node.js (v14 or higher)
- npm (Node Package Manager)

## Installation

Navigate to the tool directory and install dependencies:

```bash
cd domain-crud-generator-tool
npm install
```

## Usage

```bash
node index.js <EntityName> <basePackage> <basePath>
```

### Parameters

- `<EntityName>`: The name of your entity (PascalCase, e.g., "Product", "Customer")
- `<basePackage>`: The base Java package (e.g., "jp.brycen.domain")
- `<basePath>`: The absolute path to the Java source directory

### Example

```bash
node index.js Product jp.brycen.domain D:\Work\Projects\pubdis-spring-baseline\src\main\java
```

This will generate the following structure:

```
D:\Work\Projects\pubdis-spring-baseline\src\main\java\jp\brycen\domain\product\
├── controller\
│   └── ProductController.java
├── dto\
│   └── ProductDto.java
├── entity\
│   └── Product.java
├── repository\
│   └── ProductRepository.java
└── service\
    ├── ProductService.java
    └── implementation\
        └── ProductServiceImpl.java
```

## Generated Files

### 1. Entity (Product.java)
- Extends `GenericEntity<Long>`
- JPA annotations (`@Entity`, `@Table`, `@Id`, `@Column`)
- Lombok annotations (`@Getter`, `@Setter`, `@EqualsAndHashCode`)
- Default fields: `id`, `name`, `code`, `description`

### 2. Repository (ProductRepository.java)
- Extends `GenericRepository<Product, Long>`
- Spring Data JPA interface
- Inherits CRUD operations from GenericRepository

### 3. Service Interface (ProductService.java)
- Service interface defining business operations
- Method signatures for: `create()`, `update()`, `findById()`, `findAll()`, `findAll(Pageable)`, `deleteById()`, `existsById()`
- Returns DTOs and uses Optional for nullable results

### 4. Service Implementation (ProductServiceImpl.java)
- Implements `ProductService` interface
- Constructor injection of Repository
- Full CRUD implementation using DTO conversion methods
- `@Service`, `@Validated`, and `@Transactional` annotations
- Proper transaction handling with `@Transactional(readOnly = true)` for queries

### 5. DTO (ProductDto.java)
- Standalone DTO with audit fields (`id`, `createdAt`, `updatedAt`, `status`, `deletedAt`)
- Jakarta validation annotations (`@NotBlank`, `@Size`)
- Lombok annotations (`@Data`, `@Builder`, `@NoArgsConstructor`, `@AllArgsConstructor`)
- Fields: `name`, `code`, `description`
- **Conversion methods**: `toEntity()` and static `fromEntity()`

### 6. Controller (ProductController.java)
- Standalone REST controller with full endpoint implementation
- REST endpoints at `/api/v1/product`
- Constructor injection of Service interface
- Methods: `create()`, `update()`, `findById()`, `findAll()`, `findAll(Pageable)`, `deleteById()`, `existsById()`
- Proper HTTP status codes and `ResponseEntity` handling

## REST API Endpoints

The generated controller provides these endpoints:

- `GET /api/v1/product` - Get all entities
- `GET /api/v1/product/page` - Get all entities with pagination
- `GET /api/v1/product/{id}` - Get entity by ID
- `GET /api/v1/product/exists/{id}` - Check if entity exists
- `POST /api/v1/product` - Create new entity
- `PUT /api/v1/product/{id}` - Update existing entity
- `DELETE /api/v1/product/{id}` - Delete entity

## Customization

After generation, you can customize the generated files:

1. **Add custom fields** to Entity and DTO
2. **Add custom queries** to Repository
3. **Add business methods** to Service
4. **Add custom endpoints** to Controller
5. **Adjust validation rules** in DTO
6. **Modify conversion logic** in DTO's `toEntity()` and `fromEntity()` methods

## Pattern Overview

This tool generates a CRUD domain using:

- **GenericEntity**: Base entity with audit fields (`createdAt`, `updatedAt`, `status`, `deletedAt`)
- **GenericRepository**: Spring Data JPA repository with common queries
- **Service Interface**: Defines business operations contract
- **Service Implementation**: Full CRUD implementation with DTO conversion
- **Standalone Controller**: Full REST endpoint implementation
- **DTO with Conversion Methods**: `toEntity()` instance method and `fromEntity()` static method

## Requirements

Your project must have these base classes:

- `jp.brycen.common.entity.GenericEntity`
- `jp.brycen.common.repository.GenericRepository`

## Dependencies

The generated code requires:

- Spring Boot 3.x
- Spring Data JPA
- Lombok
- Jakarta Validation API
- Jackson

## Notes

- All generated files use UTF-8 encoding
- The tool creates directories recursively
- Existing files will NOT be overwritten
- Entity names should be in PascalCase
- Package names should follow Java conventions

## Troubleshooting

If you encounter errors:

1. **Missing dependencies**: Run `npm install` in the tool directory
2. **Permission errors**: Check write permissions on the target directory
3. **Path errors**: Use absolute paths for `<basePath>` parameter
4. **Template errors**: Ensure all template files exist in `template/` directory

## License

ISC
