const express = require("express");
const app = express();
const dotenv = require("dotenv");
const cors = require("cors");
const [compression, helmet] = [require("compression"), require("helmet")];
const path = require("path");

dotenv.config();
app.use(compression());
app.use(cors());
app.use(helmet({hidePoweredBy: false}));
app.use(express.json());
app.use(express.urlencoded({extended: false}));
app.use((req, res, next) => {
    res.set({
        "X-Powered-By": "Klang Corp.",
        "X-Server": "Knode",
        "App-Name": "",
        "App-Version": "1.0.0.0",
        "App-License": "GNU GPLv3",
        "App-Vendor": "",
        "App-Vendor-Support-Mail": "me@site.com",
        "App-Vendor-Support-Phone": "",
    });
    next();
});
app.use(express.static(path.join(__dirname, "public")));

app.get("/", (req, res) => {
    res.status(200).json({message: "Hello from Knode", success: true});
});

app.use((req, res) => {
  res.status(404).json({
    error: { code: 404, message: "404 Route Not Found" },
    success: false,
  });
});

app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: { code: 500, message: "Internal Server Error" },
    success: false,
  });
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
    console.log(`Listening on port ${PORT}`);
});
if (typeof module === "object" && !!module.exports) module.exports = app;