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
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.NNIRestServer = void 0;
const body_parser_1 = __importDefault(require("body-parser"));
const express_1 = __importDefault(require("express"));
const http_proxy_1 = __importDefault(require("http-proxy"));
const path_1 = __importDefault(require("path"));
const component = __importStar(require("../common/component"));
const restServer_1 = require("../common/restServer");
const utils_1 = require("../common/utils");
const restHandler_1 = require("./restHandler");
const experimentStartupInfo_1 = require("../common/experimentStartupInfo");
let NNIRestServer = class NNIRestServer extends restServer_1.RestServer {
    LOGS_ROOT_URL = '/logs';
    netronProxy = null;
    API_ROOT_URL = '/api/v1/nni';
    constructor() {
        super();
        this.API_ROOT_URL = experimentStartupInfo_1.getAPIRootUrl();
        this.netronProxy = http_proxy_1.default.createProxyServer();
    }
    registerRestHandler() {
        this.app.use(experimentStartupInfo_1.getPrefixUrl(), express_1.default.static('static'));
        this.app.use(body_parser_1.default.json({ limit: '50mb' }));
        this.app.use(this.API_ROOT_URL, restHandler_1.createRestHandler(this));
        this.app.use(this.LOGS_ROOT_URL, express_1.default.static(utils_1.getLogDir()));
        this.app.all('/netron/*', (req, res) => {
            delete req.headers.host;
            req.url = req.url.replace('/netron', '/');
            this.netronProxy.web(req, res, {
                changeOrigin: true,
                target: 'https://netron.app'
            });
        });
        this.app.get(`${experimentStartupInfo_1.getPrefixUrl()}/*`, (_req, res) => {
            res.sendFile(path_1.default.resolve('static/index.html'));
        });
    }
};
NNIRestServer = __decorate([
    component.Singleton,
    __metadata("design:paramtypes", [])
], NNIRestServer);
exports.NNIRestServer = NNIRestServer;
