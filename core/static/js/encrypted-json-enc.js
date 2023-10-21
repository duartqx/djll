htmx.defineExtension("encrypted-json-enc", {
  onEvent: function (name, evt) {
    if (name === "htmx:configRequest") {
      evt.detail.headers["Content-Type"] = "application/json";
    }
  },

  encodeParameters: function (xhr, parameters, elt) {
    xhr.overrideMimeType("text/json");

    let { enckey, ...unencryptedParameters } = parameters;

    const secret = new fernet.Secret(enckey);
    const token = new fernet.Token({ secret: secret });

    let encryptedValues = { enc: true };

    for (let [ key, value ] of Object.entries(unencryptedParameters)) {
      encryptedValues[key] = token.encode(value).toString();
    }

    return JSON.stringify(encryptedValues);
  },
});
