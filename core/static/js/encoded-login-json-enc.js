htmx.defineExtension("encoded-login-json-enc", {
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
      email: token.encode(parameters.email).toString(),
      password: token.encode(parameters.password).toString(),
      csrfmiddlewaretoken: parameters.csrfmiddlewaretoken,
    };

    return JSON.stringify(encryptedValues);
  },
});
