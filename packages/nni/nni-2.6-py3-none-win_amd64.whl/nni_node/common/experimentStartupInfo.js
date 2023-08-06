"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.getPrefixUrl = exports.getAPIRootUrl = exports.getDispatcherPipe = exports.isReadonly = exports.getPlatform = exports.isNewExperiment = exports.getBasePort = exports.getExperimentId = exports.setExperimentStartupInfo = exports.getExperimentStartupInfo = exports.ExperimentStartupInfo = void 0;
const assert_1 = __importDefault(require("assert"));
const os_1 = __importDefault(require("os"));
const path_1 = __importDefault(require("path"));
const API_ROOT_URL = '/api/v1/nni';
let singleton = null;
class ExperimentStartupInfo {
    experimentId = '';
    newExperiment = true;
    basePort = -1;
    initialized = false;
    logDir = '';
    logLevel = '';
    readonly = false;
    dispatcherPipe = null;
    platform = '';
    urlprefix = '';
    constructor(newExperiment, experimentId, basePort, platform, logDir, logLevel, readonly, dispatcherPipe, urlprefix) {
        this.newExperiment = newExperiment;
        this.experimentId = experimentId;
        this.basePort = basePort;
        this.platform = platform;
        if (logDir !== undefined && logDir.length > 0) {
            this.logDir = path_1.default.join(path_1.default.normalize(logDir), experimentId);
        }
        else {
            this.logDir = path_1.default.join(os_1.default.homedir(), 'nni-experiments', experimentId);
        }
        if (logLevel !== undefined && logLevel.length > 1) {
            this.logLevel = logLevel;
        }
        if (readonly !== undefined) {
            this.readonly = readonly;
        }
        if (dispatcherPipe != undefined && dispatcherPipe.length > 0) {
            this.dispatcherPipe = dispatcherPipe;
        }
        if (urlprefix != undefined && urlprefix.length > 0) {
            this.urlprefix = urlprefix;
        }
    }
    get apiRootUrl() {
        return this.urlprefix === '' ? API_ROOT_URL : `/${this.urlprefix}${API_ROOT_URL}`;
    }
    static getInstance() {
        assert_1.default(singleton !== null);
        return singleton;
    }
}
exports.ExperimentStartupInfo = ExperimentStartupInfo;
function getExperimentStartupInfo() {
    return ExperimentStartupInfo.getInstance();
}
exports.getExperimentStartupInfo = getExperimentStartupInfo;
function setExperimentStartupInfo(newExperiment, experimentId, basePort, platform, logDir, logLevel, readonly, dispatcherPipe, urlprefix) {
    singleton = new ExperimentStartupInfo(newExperiment, experimentId, basePort, platform, logDir, logLevel, readonly, dispatcherPipe, urlprefix);
}
exports.setExperimentStartupInfo = setExperimentStartupInfo;
function getExperimentId() {
    return getExperimentStartupInfo().experimentId;
}
exports.getExperimentId = getExperimentId;
function getBasePort() {
    return getExperimentStartupInfo().basePort;
}
exports.getBasePort = getBasePort;
function isNewExperiment() {
    return getExperimentStartupInfo().newExperiment;
}
exports.isNewExperiment = isNewExperiment;
function getPlatform() {
    return getExperimentStartupInfo().platform;
}
exports.getPlatform = getPlatform;
function isReadonly() {
    return getExperimentStartupInfo().readonly;
}
exports.isReadonly = isReadonly;
function getDispatcherPipe() {
    return getExperimentStartupInfo().dispatcherPipe;
}
exports.getDispatcherPipe = getDispatcherPipe;
function getAPIRootUrl() {
    return getExperimentStartupInfo().apiRootUrl;
}
exports.getAPIRootUrl = getAPIRootUrl;
function getPrefixUrl() {
    const prefix = getExperimentStartupInfo().urlprefix === '' ? '' : `/${getExperimentStartupInfo().urlprefix}`;
    return prefix;
}
exports.getPrefixUrl = getPrefixUrl;
