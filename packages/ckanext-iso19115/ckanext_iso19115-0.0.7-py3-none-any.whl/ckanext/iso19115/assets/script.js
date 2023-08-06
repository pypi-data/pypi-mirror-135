ckan.module("iso19115-check-validity", function ($, _) {
  "use strict";

  return {
    options: {
      debug: false,
	id: null,
    },

      initialize: function () {
	  $.proxyAll(this, /_on/);
	  this.el.on("click", this._onClick);
      },

      _onClick: function() {
	  this.sandbox.client.call("GET", "iso19115_package_check", "?id=" + this.options.id, this._onSuccess, this._onError);
      },

      _onSuccess: function(){

      },

      _onError: function(err){
	  const target = this.options.target ? $(this.options.target): this.sandbox.notify.el;
	  const errors = err.responseJSON.error;
	  for (let type of Object.keys(errors)) {
	      if (type.slice(0, 2) === "__") {
		  continue;
	      }
	      const msg = this.create(type, errors[type], "error");
	      this.report(msg, target);
	  }
      },

      report: function(msg, target) {

	  target.append(msg.alert());
      },

      create: function(title, problems, type){
	  var alert = $('<div class="alert fade in"><strong></strong><a class="close" data-dismiss="alert">x</a></div>');
	  alert.addClass('alert-' + (type || 'error'));
	  alert.find('strong').text(title);

	  const errors = $.map(problems, function(text) { return $('<pre class="iso-validation-report">').append($("<code>", {text}));});

	  alert.append(errors);
	  return alert;

      }
  };
});
