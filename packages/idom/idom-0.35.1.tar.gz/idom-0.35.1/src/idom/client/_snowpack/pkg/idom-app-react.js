import './common/index-6ed86a98.js';
import './common/index-21e68f69.js';
import { L as LayoutServerInfo, m as mountWithLayoutServer } from './common/server-d63eddfd.js';
import './common/htm.module-dd7abb54.js';
import './common/index-6ddd8323.js';

function mount(mountPoint) {
  const serverInfo = new LayoutServerInfo({
    host: document.location.hostname,
    port: document.location.port,
    path: "/",
    query: queryParams.user.toString(),
    secture: document.location.protocol == "https",
  });

  mountWithLayoutServer(mountPoint, serverInfo, shouldReconnect() ? 45 : 0);
}

function shouldReconnect() {
  return queryParams.reserved.get("noReconnect") === null;
}

const queryParams = (() => {
  const reservedParams = new URLSearchParams();
  const userParams = new URLSearchParams(window.location.search);

  const reservedParamNames = ["noReconnect"];
  reservedParamNames.forEach((name) => {
    const value = userParams.get(name);
    if (value !== null) {
      reservedParams.append(name, userParams.get(name));
      userParams.delete(name);
    }
  });

  return {
    reserved: reservedParams,
    user: userParams,
  };
})();

export { mount };
