(function(App) {
    'use strict';
    var querystring = require('querystring');
    var request = require('request');
    var Q = require('q');
    var http = require('http');
    var zlib = require('zlib');
    var inherits = require('util').inherits;

    var URL = false;

    function Kickxxx() {
        Kickxxx.super_.call(this);
    }

    inherits(Kickxxx, App.Providers.Generic);

    var queryTorrents = function(filters) {

        var deferred = Q.defer();

        var params = {};
        params.field = 'seeders';
        params.sorder = 'desc';

        var keyword = '';
        if (filters.keywords) {
            keyword = filters.keywords.replace(' ', '%20');
        }

        if (filters.sorder) {
            var sorder = 'desc';
            if (filters.sorder === 1) {
                sorder = 'asc';
            }
            params.sorder = sorder;
        }

        if (filters.sorter && filters.sorter !== 'popularity') {
            params.field = filters.sorter;
        }

        if (filters.page) {
            params.page = filters.page;
        }

        var url = AdvSettings.get('kickxxxApiEndpoint') + 'json.php?q=' + keyword + '%20category:xxx&' + querystring.stringify(params).replace(/%E2%80%99/g, '%27');

        win.info('Request to KICKXXX API');
        win.debug(url);
        request({
            url: url,
            json: true
        }, function(error, response, data) {
            if (error || response.statusCode >= 400) {
                deferred.reject(error);
            } else if (!data || (data.error && data.error !== 'No movies found')) {
                var err = data ? data.error : 'No data returned';
                win.error('Kickxxx error:', err);
                deferred.reject(err);
            } else {
                deferred.resolve(data.list || []);
            }
        });

        return deferred.promise;
    };


    var formatForPopcorn = function(items) {
        var results = {};
        var movieFetch = {};
        movieFetch.results = [];
        movieFetch.hasMore = (Number(items.length) > 1 ? true : false);
        _.each(items, function(movie) {
            var largeCover = 'http://morfeo.altervista.org/poster.jpg'
                //			var imdb = movie.hash.toLowerCase().slice(0,10);
            var imdb = movie.hash;
            var date = movie.pubDate.split(' ');
            var onlyear = date[3];

            // Calc torrent health
            var seeds = movie.seeds;
            var peers = movie.peers;

            var torrents = {};
            torrents['720p'] = {
                url: 'http://torcache.net/torrent/' + movie.hash + '.torrent',
                size: movie.size,
                filesize: String((movie.size / 1048576).toFixed(1)) + ' MB',
                seed: seeds,
                peer: peers
            };

            var ptItem = results[imdb];
            if (!ptItem) {
                ptItem = {
                    imdb_id: imdb,
                    title: movie.title.replace(/\([^)]*\)|1080p|DIRECTORS CUT|EXTENDED|UNRATED|3D|[()]/g, ''),
                    year: onlyear,
                    genre: 'Action',
                    rating: '5',
                    image: largeCover,
                    torrents: torrents,
                    type: 'movie'
                };

                movieFetch.results.push(ptItem);
            } else {
                _.extend(ptItem.torrents, torrents);
            }
            results[imdb] = ptItem;
        });
        return movieFetch;
    };

    // Single element query
    var queryTorrent = function(torrent_id, old_data) {
        return Q.Promise(function(resolve, reject) {
            var url = AdvSettings.get('kickxxxApiEndpointNoSsl') + '/usearch/' + torrent_id;
            var redirectionUrl;
            var redirectionPath;
            win.info('Request to Kickxxx API');
            win.debug(url);

            request({
                url: url,
                followRedirect: true
            }, function(error, response, data) {

                if (error || response.statusCode >= 400) {
                    reject(error);
                } else if (!data || (data.error && data.error !== 'No movie found')) {
                    var err = data ? data.error : 'No data returned';
                    win.error('Kickxxx error:', err);
                    reject(err);
                } else {
                    redirectionPath = response.request.response.req.path;
                    redirectionUrl = AdvSettings.get('kickxxxApiEndpointNoSsl') + redirectionPath;

                    var searchterm = redirectionPath.slice(1, redirectionPath.length - 14);
                    var singleElement = AdvSettings.get('kickxxxApiEndpoint') + 'json.php?q=' + searchterm;

                    request({
                        url: singleElement,
                        json: true
                    }, function(error, response, data) {
                        if (error || response.statusCode >= 400) {
                            reject(error);
                        } else if (!data || (data.error && data.error !== 'No movies found')) {
                            var err = data ? data.error : 'No data returned';
                            win.error('Kickxxx error:', err);
                            reject(err);
                        } else {
                            var ptt = formatForPopcorn(data.list || []);
                            var torrents = ptt.results.pop().torrents || {};
                            old_data.torrents = _.extend(old_data.torrents, torrents);
                            resolve(old_data);
                        }
                    });
                }
            });
        });
    };

    Kickxxx.prototype.extractIds = function(items) {
        return _.pluck(items.results, 'imdb_id');
    };

    Kickxxx.prototype.fetch = function(filters) {
        return queryTorrents(filters)
            .then(formatForPopcorn);
    };

    Kickxxx.prototype.detail = function(torrent_id, old_data) {
        return queryTorrent(torrent_id, old_data);
    };

    App.Providers.Kickxxx = Kickxxx;

})(window.App);