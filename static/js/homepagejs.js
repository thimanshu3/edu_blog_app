
        
function userfullpost(blogid) {
          
      var token = $.cookie('_xsrf');
      $.ajax({
        url: '/auth/home/posts/fullpost',
        headers: {'X-XSRFToken' : token },
        data:  blogid,
        dataType: "text",
        type: "post",
        success: function (data) {
          var html = data
          document.getElementById('main').innerHTML = html;
        },
        error: function () {
            alert('ajax return fail ')
        },
    }); 
  }
     
function like(blogid) {
    if(document.getElementById(blogid).classList.contains('active'))
        {
            var token = $.cookie('_xsrf');
            $.ajax({
            url: '/deletelike',
            headers: {'X-XSRFToken' : token },
            data:  blogid,
            dataType: "text",
            type: "POST",
            success: function (data) {
              /*document.getElementByClassName('far fa-thumbs-up').style.display = "none";
              */ 
              /*alert(data)*/
              data = JSON.parse(data)
              document.getElementById(blogid).innerHTML='<i class="far fa-thumbs-up"></i>'+data.cnt;
              document.getElementById(blogid).classList.remove('active');
              document.getElementById("dis"+blogid).disabled=false;
            },
            error: function () {
                alert('ajax fail')
            },
            });
        }
    else
      {
          var token = $.cookie('_xsrf');
          $.ajax({
          url: '/storelike',
          headers: {'X-XSRFToken' : token },
          data:  blogid,
          dataType: "text",
          type: "POST",
          success: function (data) {
            /*document.getElementByClassName('far fa-thumbs-up').style.display = "none";
            */ 
            data = JSON.parse(data)
            document.getElementById(blogid).innerHTML='<i class="far fa-thumbs-up"></i>'+data.cnt;
            document.getElementById(blogid).classList.add('active');
             document.getElementById("dis"+blogid).disabled=true;
          },
          error: function () {
              alert('ajax fail')
          },
          }); 
        }
	

}


function dislike(blogid) {
  
    if(document.getElementById(blogid).classList.contains('active'))
      {
          var token = $.cookie('_xsrf');
          $.ajax({
          url: '/deletedislike',
          headers: {'X-XSRFToken' : token },
          data:  blogid,
          dataType: "text",
          type: "POST",
          success: function (data) {
            /*document.getElementByClassName('far fa-thumbs-up').style.display = "none";
            */ 
            data = JSON.parse(data)
            document.getElementById(blogid).innerHTML='<i class="far fa-thumbs-down"></i>'+data.cnt;
            document.getElementById(blogid).classList.remove('active');
                document.getElementById(blogid.substring(3)).disabled=false;

          },
          error: function () {
              alert('ajax fail')
          },
          });
      }
    else
      {
        var token = $.cookie('_xsrf');
        $.ajax({
        url: '/storedislike',
        headers: {'X-XSRFToken' : token },
        data:  blogid,
        dataType: "text",
        type: "POST",
        success: function (data) {
          /*document.getElementByClassName('far fa-thumbs-up').style.display = "none";
          */ 
          
          data = JSON.parse(data)
          document.getElementById(blogid).innerHTML='<i class="far fa-thumbs-down"></i>'+data.cnt;
          document.getElementById(blogid).classList.add('active');
          document.getElementById(blogid.substring(3)).disabled=true;

        },
        error: function () {
            alert('ajax fail')
        },
        }); 
      }
  

}

  function play(){
       var audio = document.getElementById("audio");
       audio.play();
                 }
  
      	
  (function (factory) {
	if (typeof define === 'function' && define.amd) {
		// AMD
		define(['jquery'], factory);
	} else if (typeof exports === 'object') {
		// CommonJS
		factory(require('jquery'));
	} else {
		// Browser globals
		factory(jQuery);
	}
}(function ($) {

	var pluses = /\+/g;

	function encode(s) {
		return config.raw ? s : encodeURIComponent(s);
	}

	function decode(s) {
		return config.raw ? s : decodeURIComponent(s);
	}

	function stringifyCookieValue(value) {
		return encode(config.json ? JSON.stringify(value) : String(value));
	}

	function parseCookieValue(s) {
		if (s.indexOf('"') === 0) {
			// This is a quoted cookie as according to RFC2068, unescape...
			s = s.slice(1, -1).replace(/\\"/g, '"').replace(/\\\\/g, '\\');
		}

		try {
			// Replace server-side written pluses with spaces.
			// If we can't decode the cookie, ignore it, it's unusable.
			// If we can't parse the cookie, ignore it, it's unusable.
			s = decodeURIComponent(s.replace(pluses, ' '));
			return config.json ? JSON.parse(s) : s;
		} catch(e) {}
	}

	function read(s, converter) {
		var value = config.raw ? s : parseCookieValue(s);
		return $.isFunction(converter) ? converter(value) : value;
	}

	var config = $.cookie = function (key, value, options) {

		// Write

		if (value !== undefined && !$.isFunction(value)) {
			options = $.extend({}, config.defaults, options);

			if (typeof options.expires === 'number') {
				var days = options.expires, t = options.expires = new Date();
				t.setTime(+t + days * 864e+5);
			}

			return (document.cookie = [
				encode(key), '=', stringifyCookieValue(value),
				options.expires ? '; expires=' + options.expires.toUTCString() : '', // use expires attribute, max-age is not supported by IE
				options.path    ? '; path=' + options.path : '',
				options.domain  ? '; domain=' + options.domain : '',
				options.secure  ? '; secure' : ''
			].join(''));
		}

		// Read

		var result = key ? undefined : {};

		// To prevent the for loop in the first place assign an empty array
		// in case there are no cookies at all. Also prevents odd result when
		// calling $.cookie().
		var cookies = document.cookie ? document.cookie.split('; ') : [];

		for (var i = 0, l = cookies.length; i < l; i++) {
			var parts = cookies[i].split('=');
			var name = decode(parts.shift());
			var cookie = parts.join('=');

			if (key && key === name) {
				// If second argument (value) is a function it's a converter...
				result = read(cookie, value);
				break;
			}

			// Prevent storing a cookie that we couldn't decode.
			if (!key && (cookie = read(cookie)) !== undefined) {
				result[name] = cookie;
			}
		}

		return result;
	};

	config.defaults = {};

	$.removeCookie = function (key, options) {
		if ($.cookie(key) === undefined) {
			return false;
		}

		// Must not alter options, thus extending a fresh object...
		$.cookie(key, '', $.extend({}, options, { expires: -1 }));
		return !$.cookie(key);
	};

}));

     
      	(function ($) {

    var likeBtn = 'like',
        dislikeBtn = 'dislike';

    var defaults = {
        click: null,
        beforeClick: null,
        initialValue: 0,
        reverseMode: true,
        readOnly: false,
        likeBtnClass: 'like',
        dislikeBtnClass: 'dislike',
        activeClass: 'active',
        disabledClass: 'disabled'
    };

    function LikeDislike(element, options) {
        this.element = element;
        this.opts = $.extend({}, defaults, options);
        this.init();
    }

    LikeDislike.prototype = {
        init: function () {
            this.btns = $(this.element).find('.' + this.opts.likeBtnClass + ', .' + this.opts.dislikeBtnClass);
            this.readOnly(this.opts.readOnly);
            if (this.opts.initialValue !== 0) {
                var activeBtn = this.opts.initialValue === 1 ? likeBtn : dislikeBtn;
                this.btnDown(activeBtn);
            }
            return this;
        },
        readOnly: function (state) {
            var btns = this.btns;
            if (!state) {
                if (!this.opts.reverseMode) {
                    var notActiveBtns = btns.not('.' + this.opts.activeClass);
                    if (notActiveBtns.length) {
                        btns = notActiveBtns;
                    }
                }
                this.enable(btns);
            } else {
                this.disable(btns);
            }
        },
        getBtn: function (btnType) {
            if (btnType === likeBtn) {
                return $(this.element).find('.' + this.opts.likeBtnClass);
            } else if (btnType === dislikeBtn) {
                return $(this.element).find('.' + this.opts.dislikeBtnClass);
            } else {
                $.error('Wrong btnType: ' + btnType);
            }
        },
        btnDown: function (btnType) {
            var btn = this.getBtn(btnType);
            btn.addClass(this.opts.activeClass);
            if (!this.opts.reverseMode) {
                this.disable(btn);
            }
        },
        btnUp: function (btnType) {
            var btn = this.getBtn(btnType);
            btn.removeClass(this.opts.activeClass);
            if (!this.opts.reverseMode) {
                this.enable(btn);
            }
        },
        enable: function (btn) {
            var self = this;
            var opts = self.opts;

            btn.removeClass(opts.disabledClass);

            if (opts.beforeClick) {
                btn.on('beforeClick', function (event) {
                    return opts.beforeClick.call(self, event);
                });
            }

            btn.on('click', function (event) {
                var btn = $(this);

                if (opts.beforeClick && !btn.triggerHandler('beforeClick')) {
                    return false;
                }

                var btnType = btn.hasClass(opts.likeBtnClass) ? likeBtn : dislikeBtn;
                var hasActive = self.btns.hasClass(opts.activeClass);
                var isActive = btn.hasClass(opts.activeClass);

                var value = 0, l = 0, d = 0;

                if (btnType === likeBtn) {
                    if (isActive) {
                        self.btnUp(likeBtn);
                        l = -1;
                    } else {
                        if (hasActive) {
                            self.btnUp(dislikeBtn);
                            d = -1;
                        }
                        self.btnDown(likeBtn);
                        l = 1;
                        value = 1;
                    }
                } else {
                    if (isActive) {
                        self.btnUp(dislikeBtn);
                        d = -1;
                    } else {
                        if (hasActive) {
                            self.btnUp(likeBtn);
                            l = -1;
                        }
                        self.btnDown(dislikeBtn);
                        d = 1;
                        value = -1;
                    }
                }

                opts.click.call(self, value, l, d, event);
            });
        },
        disable: function (btn) {
            btn.addClass(this.opts.disabledClass);
            btn.off();
        }
    };

    $.fn.likeDislike = function (options) {
        return this.each(function () {
            if (!$.data(this, "plugin_LikeDislike")) {
                $.data(this, "plugin_LikeDislike",
                    new LikeDislike(this, options));
            }
        });
    };

})(jQuery);
     