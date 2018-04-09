// @include ./vendor/sha256.js
// @include ./vendor/ua-parser.js

(function (undefined) {
    /**
     * @param {String} trackingID
     * @constructor
     */
    var AnaliticaTracker = function (trackingID) {
        if (trackingID.length === 64) {
            this.trackingID = trackingID;
            this._userAgent = (new UAParser()).getResult();
            this.session = undefined;
            this._initSession();
            this.track();
        } else {
            console.error('AnaliticaTracker :: Invalid Tracking ID');
        }
    };

    AnaliticaTracker.prototype._generateSessionID = function () {
        var self = this;
        // Generate a unique session string that is used to uniquely identify
        // a particular user session. This retains anonymity but allows us to
        // track what a particular user did in their session.
        var sessionString = [
            self._userAgent.ua,
            (new Date()).getTime(),
            Math.floor(Math.random() * 10e9)
        ].join(':');
        return sha256(sessionString);
    };

    AnaliticaTracker.prototype._initSession = function () {
        var self = this;
        var sessionKey = self.trackingID + '_sessionJSON';
        var sessionJSON = sessionStorage[sessionKey];
        if (sessionJSON === undefined) {
            self.session = {
                id: self._generateSessionID(),
                browser: {
                    name: self._userAgent.browser.name,
                    version: self._userAgent.browser.version
                }
            };
            sessionStorage[sessionKey] = JSON.stringify(self.session);
        } else {
            self.session = JSON.parse(sessionJSON);
        }
    };

    /**
     * @param {Function} onComplete
     * @private
     */
    AnaliticaTracker.prototype._getInternetInformation = function (onComplete) {
        var callback = 'callback_' + sha256((new Date()).getTime() + '');

        var script = document.createElement('script');
        script.src = 'https://ipinfo.io/?callback=' + callback;

        window[callback] = function (response) {
            onComplete(response);
            // Remove script element and callback function.
            script.parentNode.removeChild(script);
            delete window[callback];
        };

        document.getElementsByTagName('head')[0].appendChild(script);
    };

    /**
     * @param {Function} onComplete
     * @private
     */
    AnaliticaTracker.prototype._generateVisit = function (onComplete) {
        var self = this;
        var trackingInformation = {
            url: window.location.href.split('?')[0],
            screen_resolution: [
                window.screen.availWidth,
                window.screen.availHeight
            ].join(',')
        };
        self._getInternetInformation(function (response) {
            trackingInformation.ip = response.ip;
            trackingInformation.country = response.country;
            onComplete(trackingInformation);
        });
    };

    AnaliticaTracker.prototype.track = function () {
        var self = this;
        self._generateVisit(function (visit) {
            var xhr = new XMLHttpRequest();
            xhr.open('POST', AnaliticaTracker.TRACKING_URL, true);
            xhr.setRequestHeader('Content-Type', 'application/json');
            xhr.onreadystatechange = function () {
                if (xhr.readyState === 4 && xhr.status === 200) {
                    try {
                        JSON.parse(xhr.responseText);
                    } catch (error) {
                        console.error(error);
                    }
                }
            };
            var data = {
                'tracking_id': self.trackingID,
                'session': self.session,
                'visit': visit
            };
            xhr.send(JSON.stringify(data));
        });
    };

    AnaliticaTracker.TRACKING_URL = 'http://localhost:8000/api/track/';

    window.AnaliticaTracker = AnaliticaTracker;
})();