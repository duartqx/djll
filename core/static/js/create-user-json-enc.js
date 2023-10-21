htmx.defineExtension("create-user-json-enc", {
  onEvent: function (name, evt) {
    if (name === "htmx:configRequest") {
      evt.detail.headers["Content-Type"] = "application/json";
    }
  },

  encodeParameters: function (xhr, parameters, elt) {
    xhr.overrideMimeType("text/json");

    const secret = new fernet.Secret(parameters.enckey);
    const token = new fernet.Token({ secret: secret });

    let encryptedValues = {
      enc: true,
      email: token.encode(email).toString(),
      password: token.encode(password).toString(),
      first_name: token.encode(first_name).toString(),
      last_name: token.encode(last_name).toString(),
    };

    return JSON.stringify(encryptedValues);
  },
});
