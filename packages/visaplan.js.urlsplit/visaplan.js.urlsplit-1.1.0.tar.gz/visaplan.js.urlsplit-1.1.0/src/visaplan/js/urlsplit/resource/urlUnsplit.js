/* visaplan.js.urlsplit: urlunsplit function
 *
 * Currently, this simply returns a URL string (which should,
 * wenn fed to urlSplit, yield something like the given object).
 *
 * There is not much intelligence (yet?); e.g., we completely ignore
 * the queryList and queryObject attributes.
 * Please take care for a reasonable query attribute yourself.
 *
 * See ./urlSplit.js
 */
function urlUnsplit (o) {
    var result='', tmp1, tmp2;
    tmp1 = o.domain;
    if (tmp1) {
        // protocol, authorization and port require a domain, right?
        tmp2 = o.protocol;
        if (tmp2)
            result += tmp2 + ':';
        result += '//';
        tmp2 = o.authorization;
        if (tmp2)
            result += tmp2 + '@';
        if (tmp1)
            result += tmp1;
        tmp2 = o.port;
        if (tmp2)
            result += ':'+tmp2;
    }
    tmp1 = o.path;
    if (tmp1)
        result += tmp1;
    tmp1 = o.query;
    if (tmp1)
        result += '?'+tmp1;
    tmp1 = o.fragment;
    if (tmp1)
        result += '#'+tmp1;
    return result;
}
