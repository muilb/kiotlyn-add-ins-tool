const fs = require('fs');
const Handlebars = require('handlebars');

var ucName = process.argv[2]
var desDir = process.argv[3];
if (desDir == undefined) {
    console.log('Put Full path for destination');
    process.exit(0);
}
var mkDir = require('./makedir');
var writeTemplate = require('./write_template');
/** kiem tra thu muc add_ins da ton tai?
 * Neu chua tao moi
 */
var add_ins = desDir + '/add_ins';
mkDir(add_ins);
// check ucName if need
var lc_ucName = ucName.toLowerCase();
var lc1_ucName = lowcaseFirts(ucName);
var ucPath = add_ins + '/' + lc_ucName;
var check = mkDir(ucPath);
if (check == undefined) {
    console.log(`Add-ins ${ucPath} already exit.`);
    process.exit(0);
}
/** Make Structure here
│   │   └── application                         <-- Application services
│   │   │   └── repositories                    <-- Data access interfaces
│   │   │       └── I{ucName}Repository.ts   1
│   │   │   └── use_cases                       <-- Application business use cases
│   │   │       └── lowcase(ucName)
│   │   │           └── Template{ucName}.ts  2
│   │   └── domain                              <-- Core business layer
│   │   │   └── entities                        <-- Domain Entities 
│   │   │       └── {ucName}.ts              3 
│   │   └── infrastructure                      <-- Extension to ExpressJS
│   │   │   └── webserver                       <-- Web Server (ExpressJS) interfaces
│   │   │       └── routers                     <-- ExpressJS Routers
│   │   │           └── lowcase(ucName)
│   │   │               └── {ucName}Router.ts    4
│   │   └── interfaces                          <-- Extension to ExpressJS
│   │   │   └── controllers                     <-- Logic routers
│   │   │       └── {ucName}Controller.ts    5
│   │   │   └── repositories                    <-- Data Access implementations
│   │   │       └── {ucName}Repository.ts    6
 */
var appPath = mkDir(ucPath + '/application');
var domainPath = mkDir(ucPath + '/domain');
var infrastructurePath = mkDir(ucPath + '/infrastructure');
var interfacesPath = mkDir(ucPath + '/interfaces');
var replicated = {
    hu3s_ucname: ucName,
    hu3s_lc_ucname: lc_ucName,
    hu3s_lc1_ucname: lc1_ucName
}
/** application folder */
var appRepo = mkDir(appPath + '/repositories');

var i_repo = appRepo + `/I${ucName}Repository.ts`
writeTemplate(i_repo, 'template/IRepository.txt', replicated);

var use_cases = mkDir(appPath + '/use_cases');
var appUcPath = mkDir(use_cases + `/${lc_ucName}`);

var tmpUc = appUcPath + `/Template${ucName}.ts`;
writeTemplate(tmpUc, 'template/TemplateUseCase.txt', replicated);

/** domain folder */
var domainEntry = mkDir(domainPath + '/entities');

var model = domainEntry + `/${ucName}.ts`
writeTemplate(model, 'template/Model.txt', replicated);

/** infrastructure folder */
var webserver = mkDir(infrastructurePath + '/webserver');
var routers = mkDir(webserver + '/routers');
routers = mkDir(routers + `/${lc_ucName}`)
var ucRouter = routers + `/${ucName}Router.ts`
writeTemplate(ucRouter, 'template/Router.txt', replicated);

/** interfaces folder */
var controllers = mkDir(interfacesPath + '/controllers');

var control = controllers + `/${ucName}Controller.ts`
writeTemplate(control, 'template/Controller.txt', replicated);

var dbRepo = mkDir(interfacesPath + '/repositories');

var repo = dbRepo + `/${ucName}Repository.ts`
writeTemplate(repo, 'template/Repository.txt', replicated);

function lowcaseFirts(str) {
    return str.charAt(0).toLowerCase() + str.slice(1);
}

