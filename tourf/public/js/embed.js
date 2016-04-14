if (window.__rivaltree === undefined) {
	!function(doc, win) {
		window.__rivaltree = {
			ev: (doc.addEventListener !== undefined ? {
				add: 'addEventListener',
				rem: 'removeEventListener',
				pre: ''
			} : {
				add: 'attachEvent',
				rem: 'detachEvent',
				pre: 'on'
			}),
			ajax: {
				isIE8: (win.XDomainRequest !== undefined ? true : false),
				IEVersion: (function() {
					var a = navigator.userAgent.toLowerCase();
					return a.indexOf('msie') !== -1 ? parseInt(a.split('msie')[1],10) : false;
				})(),
				get: function(url, data, callback) {
					var xhr = (__rivaltree.ajax.isIE8 === true ? new win.XDomainRequest() : new XMLHttpRequest()),
						handler = function(e) {
							if (xhr.readyState === 4 && xhr.status === 200) {
								response();
							}
						},
						response = function() {
							if (typeof(callback) === 'function') {
								callback(data, xhr.responseText);
							}
						};
					try {
						if (__rivaltree.ajax.isIE8 === true) {
							xhr.onload = response;
							xhr.open('GET', url, true);
							xhr.onprogress = function(){};
							xhr.ontimeout = function(){};
							xhr.onerror = function(){};
							setTimeout(function(){xhr.send();}, 0);
						} else {
							xhr.open('GET', url, true);
							xhr.onreadystatechange = handler;
							xhr.send();
						}
					} catch(e) {
						console.log(e);
					}
				}
			},
			getElementsByClassName: function(c, s) {
				if (s === undefined) {
					s = doc;
				}
				return doc.getElementsByClassName !== undefined ? s.getElementsByClassName(c) : s.querySelectorAll('.'+c);
			},
			classFactor: function(e, c) {
				var s = e.className.split(' '),
					r = [];
				c = c.toLowerCase();
				for (var i = 0, l = s.length; i < l; i++) {
					if (s[i] !== '' && s[i].toLowerCase() !== c) {
						r.push(s[i]);
					}
				}
				return r;
			},
			addClass: function(e, c) {
				var r = __rivaltree.classFactor(e, c);
				r.push(c);
				e.className = r.join(' ');
				return e.className;
			},
			removeClass: function(e, c) {
				var r = __rivaltree.classFactor(e, c);
				e.className = r.join(' ');
				return e.className;
			},
			hasClass: function(e, c) {
				return RegExp('^(\\s*.+\\s+)*'+c+'(\\s+.+\\s*)*$', 'i').test(e.className);
			},
			camelize: function(s) {
				return s.replace(/[\-\s_](\w)/g, function(d, l) {
					return l.toUpperCase();
				});
			},
			getStyle: function(e, s) {
				var c = __rivaltree.camelize(s);
				if (e.style[c] !== '') {
					return e.style[c];
				}
				if (e.currentStyle === undefined) {
					return doc.defaultView.getComputedStyle(e, null).getPropertyValue(s);
				}
				return e.currentStyle(c);
			},
			WebSocket: function(url, options) {
				var op = {
						reconnect: true,
						reconnectAttempts: 5,
						reconnectInterval: 3000,
						onopen: null,
						onmessage: null,
						onerror: null,
						onclose: null,
					},
					rc = {
						attempts: 0,
						interval: null,
					},
					ws = new WebSocket(url);

				if (typeof options === 'object') {
					for (var key in options) {
						if (key in op === true) {
							op[key] = options[key];
						}
					}
				}

				function reconnect() {
					if (rc.attempts < op.reconnectAttempts) {
						// TODO: Still need to finish this
						rc.attempts++;
						rc.interval = setTimeout(reconnect, op.reconnectInterval);
					}
				}

				ws.onopen = function() {
					console.log('websocket connected');
					if (rc.interval !== null) {
						clearTimeout(rc.interval);
						rc.interval = null;
					}
					if ('onopen' in op === true && typeof op.onopen === 'function') {
						op.onopen();
					}
				};
				ws.onmessage = function(e) {
					console.log('Received: ' + e.data);
					if ('onmessage' in op === true && typeof op.onmessage === 'function') {
						op.onmessage(e.data);
					}
				};
				ws.onerror = function(e) {
					console.error(e);
					if ('onerror' in op === true && typeof op.onerror === 'function') {
						op.onerror(e);
					}
				};
				ws.onclose = function(e) {
					console.log('connection closed');
					if (op.reconnect === true) {
						rc.attempts = 0;
						reconnect();
					}
					if ('onclose' in op === true && typeof op.onclose === 'function') {
						op.onclose(e);
					}
				}
				this.sendMessage = function(msg) {
					console.log('send message', msg);
					ws.send(msg);
				};
			},
			isMobile: (function() {
				var a = navigator.userAgent || navigator.vendor || win.opera;
				return /(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows (ce|phone)|xda|xiino/i.test(a) || /1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0, 4));
			})(),
		};
	}(document, window);
}

if (window.__rte === undefined) {
	!function(doc, win) {
		window.__rte = {
			inited: false,
			socket: null,
			widgets: [],
			brackets: {},
			injectResponse: function(id, mk) {
				__rte.widgets[id].innerHTML = mk;
				__rte.widgets[id].setAttribute('data-widget-uid', id);

				var bracket_id = __rte.widgets[id].getAttribute('data-bracket-id');
				if (__rte.brackets[bracket_id] === undefined) {
					__rte.brackets[bracket_id] = [__rte.widgets[id]];
				} else {
					__rte.brackets[bracket_id].push(__rte.widgets[id]);
				}
			},
			click: function(e) {
				var t = e.target || e.srcElement;
			},
			update: function(bracket, games, teams, phase) {
				// Show/hide elimination bracket based on phase[0]
				var elims = bracket.querySelectorAll('.rte-bracket, .rte-bracket-header');
				for (var i = 0, l = elims.length; i < l; i++) {
					var hasClass = __rivaltree.hasClass(elims[i], 'rte-hidden');
					if (phase[0] < 3 && hasClass === false) {
						__rivaltree.addClass(elims[i], 'rte-hidden');
					} else if (phase[0] > 2 && hasClass === true) {
						__rivaltree.removeClass(elims[i], 'rte-hidden');
					}
				}
				// Iterate through each game in games, using id and team attributes for update vectors
				for (var i = 0, l = games.length; i < l; i++) {
					if (games[i].type === 'round_robin') {
						var wins = bracket.querySelectorAll('[data-game-id="'+games[i].id+'"] [data-team]');
						for (var j = 0, k = wins.length; j < k; j++) {
							var data = games[i]['team'+wins[j].getAttribute('data-team')];
							wins[j].textContent = data.wins;
							if (data.is_winner === true) {
								__rivaltree.addClass(wins[j], 'rte-winner');
								__rivaltree.addClass(wins[j].previousElementSibling, 'rte-winner');
							} else {
								__rivaltree.removeClass(wins[j], 'rte-winner');
								__rivaltree.removeClass(wins[j].previousElementSibling, 'rte-winner');
							}
						}
					} else {
						var wraps = bracket.querySelectorAll('[data-game-id="'+games[i].id+'"]');
						for (var j = 0, k = wraps.length; j < k; j++) {
							var data = games[i]['team'+wraps[j].getAttribute('data-team')],
								nodes = wraps[j].querySelectorAll('.rte-wins, .rte-team');
							if (data.is_winner === true) {
								__rivaltree.addClass(wraps[j], 'rte-winner');
							} else {
								__rivaltree.removeClass(wraps[j], 'rte-winner');
							}
							for (var n = 0, m = nodes.length; n < m; n++) {
								if (__rivaltree.hasClass(nodes[n], 'rte-wins') === true) {
									nodes[n].textContent = data.id === null ? '' : data.wins;
								} else if (__rivaltree.hasClass(nodes[n], 'rte-team') === true) {
									nodes[n].textContent = data.id === null ? '#'+data.seed : teams[data.id].name;
								}
							}
						}
					}
				}
			},
			init: function(e) {
				if (e !== undefined && e.type === 'readystatechange' && doc.readyState !== 'complete') {
					return;
				}

				var ev = __rivaltree.ev,
					ws = __rivaltree.getElementsByClassName('rivaltree-widget'),
					src = document.getElementById('rivaltree-script').src.split('static/js/embed.js')[0];

				for (var i = 0, l = ws.length; i < l; i++) {
					__rte.widgets[i] = ws[i];

					if (ws[i].getAttribute('data-widget-uid') !== null) {
						continue;
					}

					__rivaltree.ajax.get(src + 'embed/' + ws[i].getAttribute('data-bracket-id') + '/' + (__rivaltree.isMobile === true ? '?mobile' : ''), {uid:i}, function(params, data) {
						try {
							if (__rte.widgets[params.uid].getAttribute('data-widget-uid') !== null) {
								return;
							}
							__rte.injectResponse(params.uid, data);
						} catch (err){}

						if (window.WebSocket !== undefined && __rte.socket === null) {
							__rte.socket = new __rivaltree.WebSocket('ws://rivaltree.com:9000/', {
								onopen: function() {
									for (var i = 0, l = __rte.widgets.length; i < l; i++) {
										if (__rte.widgets[i].getAttribute('data-subscribed') !== 'true') {
											__rte.widgets[i].setAttribute('data-subscribed', false);
											__rte.socket.sendMessage(JSON.stringify({type:'SUB', bracket_id:__rte.widgets[i].getAttribute('data-bracket-id')}));
										}
									}
								},
								onmessage: function(data) {
									data = JSON.parse(data);
									if (data.type === 'SUB') {
										for (var i = 0, l = __rte.widgets.length; i < l; i++) {
											if (__rte.widgets[i].getAttribute('data-bracket-id') === data.bracket_id) {
												__rte.widgets[i].setAttribute('data-subscribed', true);
											}
										}
									} else if (data.type === 'PUB' && __rte.brackets[data.bracket_id] !== undefined) {
										for (var i = 0, l = __rte.brackets[data.bracket_id].length; i < l; i++) {
											__rte.update(__rte.brackets[data.bracket_id][i], data.games, data.teams, data.phase);
										}
									}
								},
							});
						}
					});
				}

				if (__rte.inited === false) {
					doc[ev.rem](ev.pre+'DOMContentLoaded', __rte.init, false);
					doc[ev.rem](ev.pre+'readystatechange', __rte.init, false);
					win[ev.rem](ev.pre+'load', __rte.init, false);
					doc[ev.add](ev.pre+(__rivaltree.isMobile === true ? 'touchstart' : 'click'), __rte.click, true);

					__rte.inited = true;
				}
			},
		};
	}(document, window);
}

!function(d, w) {
	if (document.readyState === 'complete') {
		__rte.init();
	} else {
		var e = __rivaltree.ev;
		d[e.add](e.pre+'DOMContentLoaded', __rte.init, false);
		d[e.add](e.pre+'readystatechange', __rte.init, false);
		w[e.add](e.pre+'load', __rte.init, false);
	}
}(document, window);
