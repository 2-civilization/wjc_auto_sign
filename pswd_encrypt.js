const CryptoJS = require('crypto-js')

function getAesString(data, key0, iv0) {
    key0 = key0.replace(/(^\s+)|(\s+$)/g, "");
    var key = CryptoJS.enc.Utf8.parse(key0);
    var iv = CryptoJS.enc.Utf8.parse(iv0);
    var encrypted = CryptoJS.AES.encrypt(data, key, {
        iv: iv,
        mode: CryptoJS.mode.CBC,
        padding: CryptoJS.pad.Pkcs7
    });
    return encrypted.toString();
}
function encryptAES(data, aesKey) {
    if (!aesKey) {
        return data;
    }
    var encrypted = getAesString(randomString(64) + data, aesKey, randomString(16));
    return encrypted;
}
var $aes_chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678';
var aes_chars_len = $aes_chars.length;
function randomString(len) {
    var retStr = '';
    for (i = 0; i < len; i++) {
        retStr += $aes_chars.charAt(Math.floor(Math.random() * aes_chars_len));
    }
    return retStr;
}


exports.encryptAES = encryptAES;

// pswd = '1234566566'
// salt = 's96jl3yh5EybDRKT'
// console.log(encryptAES(pswd,salt))


