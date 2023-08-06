"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", { value: true });
require("app-module-path/register");
const typescript_ioc_1 = require("typescript-ioc");
const fs = __importStar(require("fs"));
const path = __importStar(require("path"));
const component = __importStar(require("./common/component"));
const datastore_1 = require("./common/datastore");
const experimentStartupInfo_1 = require("./common/experimentStartupInfo");
const log_1 = require("./common/log");
const manager_1 = require("./common/manager");
const experimentManager_1 = require("./common/experimentManager");
const tensorboardManager_1 = require("./common/tensorboardManager");
const utils_1 = require("./common/utils");
const nniDataStore_1 = require("./core/nniDataStore");
const nnimanager_1 = require("./core/nnimanager");
const sqlDatabase_1 = require("./core/sqlDatabase");
const nniExperimentsManager_1 = require("./core/nniExperimentsManager");
const nniTensorboardManager_1 = require("./core/nniTensorboardManager");
const nniRestServer_1 = require("./rest_server/nniRestServer");
function initStartupInfo(startExpMode, experimentId, basePort, platform, logDirectory, experimentLogLevel, readonly, dispatcherPipe, urlprefix) {
    const createNew = (startExpMode === manager_1.ExperimentStartUpMode.NEW);
    experimentStartupInfo_1.setExperimentStartupInfo(createNew, experimentId, basePort, platform, logDirectory, experimentLogLevel, readonly, dispatcherPipe, urlprefix);
}
async function initContainer(foreground, _platformMode, logFileName) {
    typescript_ioc_1.Container.bind(manager_1.Manager)
        .to(nnimanager_1.NNIManager)
        .scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(datastore_1.Database)
        .to(sqlDatabase_1.SqlDB)
        .scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(datastore_1.DataStore)
        .to(nniDataStore_1.NNIDataStore)
        .scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(experimentManager_1.ExperimentManager)
        .to(nniExperimentsManager_1.NNIExperimentsManager)
        .scope(typescript_ioc_1.Scope.Singleton);
    typescript_ioc_1.Container.bind(tensorboardManager_1.TensorboardManager)
        .to(nniTensorboardManager_1.NNITensorboardManager)
        .scope(typescript_ioc_1.Scope.Singleton);
    const DEFAULT_LOGFILE = path.join(utils_1.getLogDir(), 'nnimanager.log');
    if (!foreground) {
        if (logFileName === undefined) {
            log_1.startLogging(DEFAULT_LOGFILE);
        }
        else {
            log_1.startLogging(logFileName);
        }
    }
    log_1.setLogLevel(logLevel);
    const ds = component.get(datastore_1.DataStore);
    await ds.init();
}
function usage() {
    console.info('usage: node main.js --port <port> --mode \
    <local/remote/pai/kubeflow/frameworkcontroller/aml/adl/hybrid/dlc> --start_mode <new/resume> --experiment_id <id> --foreground <true/false>');
}
const strPort = utils_1.parseArg(['--port', '-p']);
if (!strPort || strPort.length === 0) {
    usage();
    process.exit(1);
}
const foregroundArg = utils_1.parseArg(['--foreground', '-f']);
if (foregroundArg && !['true', 'false'].includes(foregroundArg.toLowerCase())) {
    console.log(`FATAL: foreground property should only be true or false`);
    usage();
    process.exit(1);
}
const foreground = (foregroundArg && foregroundArg.toLowerCase() === 'true') ? true : false;
const port = parseInt(strPort, 10);
const mode = utils_1.parseArg(['--mode', '-m']);
const startMode = utils_1.parseArg(['--start_mode', '-s']);
if (![manager_1.ExperimentStartUpMode.NEW, manager_1.ExperimentStartUpMode.RESUME].includes(startMode)) {
    console.log(`FATAL: unknown start_mode: ${startMode}`);
    usage();
    process.exit(1);
}
const experimentId = utils_1.parseArg(['--experiment_id', '-id']);
if (experimentId.trim().length < 1) {
    console.log(`FATAL: cannot resume the experiment, invalid experiment_id: ${experimentId}`);
    usage();
    process.exit(1);
}
const logDir = utils_1.parseArg(['--log_dir', '-ld']);
if (logDir.length > 0) {
    if (!fs.existsSync(logDir)) {
        console.log(`FATAL: log_dir ${logDir} does not exist`);
    }
}
const logLevel = utils_1.parseArg(['--log_level', '-ll']);
const readonlyArg = utils_1.parseArg(['--readonly', '-r']);
if (readonlyArg && !['true', 'false'].includes(readonlyArg.toLowerCase())) {
    console.log(`FATAL: readonly property should only be true or false`);
    usage();
    process.exit(1);
}
const readonly = (readonlyArg && readonlyArg.toLowerCase() == 'true') ? true : false;
const dispatcherPipe = utils_1.parseArg(['--dispatcher_pipe']);
const urlPrefix = utils_1.parseArg(['--url_prefix']);
initStartupInfo(startMode, experimentId, port, mode, logDir, logLevel, readonly, dispatcherPipe, urlPrefix);
utils_1.mkDirP(utils_1.getLogDir())
    .then(async () => {
    try {
        await initContainer(foreground, mode);
        const restServer = component.get(nniRestServer_1.NNIRestServer);
        await restServer.start();
        log_1.getLogger('main').info(`Rest server listening on: ${restServer.endPoint}`);
    }
    catch (err) {
        log_1.getLogger('main').error(`${err.stack}`);
        throw err;
    }
})
    .catch((err) => {
    console.error(`Failed to create log dir: ${err.stack}`);
});
function cleanUp() {
    component.get(manager_1.Manager).stopExperiment();
}
process.on('SIGTERM', cleanUp);
process.on('SIGBREAK', cleanUp);
process.on('SIGINT', cleanUp);
