import { r as react } from './index-6ed86a98.js';
import { r as reactDom } from './index-21e68f69.js';
import { h as htm } from './htm.module-dd7abb54.js';
import { j as jsonpatch } from './index-6ddd8323.js';

function useJsonPatchCallback(initial) {
  const doc = react.useRef(initial);
  const forceUpdate = useForceUpdate();

  const applyPatch = react.useCallback(
    (path, patch) => {
      if (!path) {
        // We CANNOT mutate the part of the document because React checks some
        // attributes of the model (e.g. model.attributes.style is checked for
        // identity).
        doc.current = applyNonMutativePatch(
          doc.current,
          patch);
      } else {
        // We CAN mutate the document here though because we know that nothing above
        // The patch `path` is changing. Thus, maintaining the identity for that section
        // of the model is accurate.
        applyMutativePatch(doc.current, [
          {
            op: "replace",
            path: path,
            // We CANNOT mutate the part of the document where the actual patch is being
            // applied. Instead we create a copy because React checks some attributes of
            // the model (e.g. model.attributes.style is checked for identity). The part
            // of the document above the `path` can be mutated though because we know it
            // has not changed.
            value: applyNonMutativePatch(
              jsonpatch.getValueByPointer(doc.current, path),
              patch
            ),
          },
        ]);
      }
      forceUpdate();
    },
    [doc]
  );

  return [doc.current, applyPatch];
}

function applyNonMutativePatch(doc, patch) {
  return jsonpatch.applyPatch(doc, patch, false, false, true).newDocument;
}

function applyMutativePatch(doc, patch) {
  jsonpatch.applyPatch(doc, patch, false, true, true).newDocument;
}

function useForceUpdate() {
  const [, updateState] = react.useState();
  return react.useCallback(() => updateState({}), []);
}

function serializeEvent(event) {
  const data = {};

  if (event.type in eventTransforms) {
    Object.assign(data, eventTransforms[event.type](event));
  }

  data.target = serializeDomElement(event.target);
  data.currentTarget =
    event.target === event.currentTarget
      ? data.target
      : serializeDomElement(event.currentTarget);
  data.relatedTarget = serializeDomElement(event.relatedTarget);

  return data;
}

function serializeDomElement(element) {
  let elementData = null;
  if (element) {
    elementData = defaultElementTransform(element);
    if (element.tagName in elementTransforms) {
      elementTransforms[element.tagName].forEach((trans) =>
        Object.assign(elementData, trans(element))
      );
    }
  }
  return elementData;
}

const elementTransformCategories = {
  hasValue: (element) => ({
    value: element.value,
  }),
  hasCurrentTime: (element) => ({
    currentTime: element.currentTime,
  }),
  hasFiles: (element) => {
    if (element?.type === "file") {
      return {
        files: Array.from(element.files).map((file) => ({
          lastModified: file.lastModified,
          name: file.name,
          size: file.size,
          type: file.type,
        })),
      };
    } else {
      return {};
    }
  },
};

function defaultElementTransform(element) {
  return { boundingClientRect: element.getBoundingClientRect() };
}

const elementTagCategories = {
  hasValue: [
    "BUTTON",
    "INPUT",
    "OPTION",
    "LI",
    "METER",
    "PROGRESS",
    "PARAM",
    "SELECT",
    "TEXTAREA",
  ],
  hasCurrentTime: ["AUDIO", "VIDEO"],
  hasFiles: ["INPUT"],
};

const elementTransforms = {};

Object.keys(elementTagCategories).forEach((category) => {
  elementTagCategories[category].forEach((type) => {
    const transforms =
      elementTransforms[type] || (elementTransforms[type] = []);
    transforms.push(elementTransformCategories[category]);
  });
});

function EventTransformCategories() {
  this.clipboard = (event) => ({
    clipboardData: event.clipboardData,
  });
  this.composition = (event) => ({
    data: event.data,
  });
  this.keyboard = (event) => ({
    altKey: event.altKey,
    charCode: event.charCode,
    ctrlKey: event.ctrlKey,
    key: event.key,
    keyCode: event.keyCode,
    locale: event.locale,
    location: event.location,
    metaKey: event.metaKey,
    repeat: event.repeat,
    shiftKey: event.shiftKey,
    which: event.which,
  });
  this.mouse = (event) => ({
    altKey: event.altKey,
    button: event.button,
    buttons: event.buttons,
    clientX: event.clientX,
    clientY: event.clientY,
    ctrlKey: event.ctrlKey,
    metaKey: event.metaKey,
    pageX: event.pageX,
    pageY: event.pageY,
    screenX: event.screenX,
    screenY: event.screenY,
    shiftKey: event.shiftKey,
  });
  this.pointer = (event) => ({
    ...this.mouse(event),
    pointerId: event.pointerId,
    width: event.width,
    height: event.height,
    pressure: event.pressure,
    tiltX: event.tiltX,
    tiltY: event.tiltY,
    pointerType: event.pointerType,
    isPrimary: event.isPrimary,
  });
  this.selection = () => {
    return { selectedText: window.getSelection().toString() };
  };
  this.touch = (event) => ({
    altKey: event.altKey,
    ctrlKey: event.ctrlKey,
    metaKey: event.metaKey,
    shiftKey: event.shiftKey,
  });
  this.ui = (event) => ({
    detail: event.detail,
  });
  this.wheel = (event) => ({
    deltaMode: event.deltaMode,
    deltaX: event.deltaX,
    deltaY: event.deltaY,
    deltaZ: event.deltaZ,
  });
  this.animation = (event) => ({
    animationName: event.animationName,
    pseudoElement: event.pseudoElement,
    elapsedTime: event.elapsedTime,
  });
  this.transition = (event) => ({
    propertyName: event.propertyName,
    pseudoElement: event.pseudoElement,
    elapsedTime: event.elapsedTime,
  });
}

const eventTypeCategories = {
  clipboard: ["copy", "cut", "paste"],
  composition: ["compositionend", "compositionstart", "compositionupdate"],
  keyboard: ["keydown", "keypress", "keyup"],
  mouse: [
    "click",
    "contextmenu",
    "doubleclick",
    "drag",
    "dragend",
    "dragenter",
    "dragexit",
    "dragleave",
    "dragover",
    "dragstart",
    "drop",
    "mousedown",
    "mouseenter",
    "mouseleave",
    "mousemove",
    "mouseout",
    "mouseover",
    "mouseup",
  ],
  pointer: [
    "pointerdown",
    "pointermove",
    "pointerup",
    "pointercancel",
    "gotpointercapture",
    "lostpointercapture",
    "pointerenter",
    "pointerleave",
    "pointerover",
    "pointerout",
  ],
  selection: ["select"],
  touch: ["touchcancel", "touchend", "touchmove", "touchstart"],
  ui: ["scroll"],
  wheel: ["wheel"],
  animation: ["animationstart", "animationend", "animationiteration"],
  transition: ["transitionend"],
};

const eventTransforms = {};

const eventTransformCategories = new EventTransformCategories();
Object.keys(eventTypeCategories).forEach((category) => {
  eventTypeCategories[category].forEach((type) => {
    eventTransforms[type] = eventTransformCategories[category];
  });
});

function createElementChildren(model, createElement) {
  if (!model.children) {
    return [];
  } else {
    return model.children
      .filter((x) => x) // filter nulls
      .map((child) => {
        switch (typeof child) {
          case "object":
            return createElement(child);
          case "string":
            return child;
        }
      });
  }
}

function createElementAttributes(model, sendEvent) {
  const attributes = Object.assign({}, model.attributes);

  if (model.eventHandlers) {
    for (const [eventName, eventSpec] of Object.entries(model.eventHandlers)) {
      attributes[eventName] = createEventHandler(sendEvent, eventSpec);
    }
  }

  return attributes;
}

function createEventHandler(sendEvent, eventSpec) {
  return function () {
    const data = Array.from(arguments).map((value) => {
      if (typeof value === "object" && value.nativeEvent) {
        if (eventSpec["preventDefault"]) {
          value.preventDefault();
        }
        if (eventSpec["stopPropagation"]) {
          value.stopPropagation();
        }
        return serializeEvent(value);
      } else {
        return value;
      }
    });
    sendEvent({
      data: data,
      target: eventSpec["target"],
    });
  };
}

function loadModelImportSource(layoutContext, importSource) {
  return layoutContext
    .loadImportSource(importSource.source, importSource.sourceType)
    .then((module) => {
      if (typeof module.bind === "function") {
        return {
          data: importSource,
          bind: (node) => {
            const shortImportSource = {
              source: importSource.source,
              sourceType: importSource.sourceType,
            };
            const binding = module.bind(node, layoutContext);
            if (
              typeof binding.create === "function" &&
              typeof binding.render === "function" &&
              typeof binding.unmount === "function"
            ) {
              return {
                render: (model) =>
                  binding.render(
                    createElementFromModuleBinding(
                      layoutContext,
                      importSource,
                      module,
                      binding,
                      model
                    )
                  ),
                unmount: binding.unmount,
              };
            } else {
              console.error(
                `${importSource.source} returned an impropper binding`
              );
            }
          },
        };
      } else {
        console.error(
          `${importSource.source} did not export a function 'bind'`
        );
      }
    });
}

function createElementFromModuleBinding(
  layoutContext,
  currentImportSource,
  module,
  binding,
  model
) {
  let type;
  if (model.importSource) {
    if (!isImportSourceEqual(currentImportSource, model.importSource)) {
      console.error(
        "Parent element import source " +
          stringifyImportSource(currentImportSource) +
          " does not match child's import source " +
          stringifyImportSource(model.importSource)
      );
      return null;
    } else if (!module[model.tagName]) {
      console.error(
        "Module from source " +
          stringifyImportSource(currentImportSource) +
          ` does not export ${model.tagName}`
      );
      return null;
    } else {
      type = module[model.tagName];
    }
  } else {
    type = model.tagName;
  }
  return binding.create(
    type,
    createElementAttributes(model, layoutContext.sendEvent),
    createElementChildren(model, (child) =>
      createElementFromModuleBinding(
        layoutContext,
        currentImportSource,
        module,
        binding,
        child
      )
    )
  );
}

function isImportSourceEqual(source1, source2) {
  return (
    source1.source === source2.source &&
    source1.sourceType === source2.sourceType
  );
}

function stringifyImportSource(importSource) {
  return JSON.stringify({
    source: importSource.source,
    sourceType: importSource.sourceType,
  });
}

const html = htm.bind(react.createElement);
const LayoutContext = react.createContext({
  sendEvent: undefined,
  loadImportSource: undefined,
});

function Layout({ saveUpdateHook, sendEvent, loadImportSource }) {
  const [model, patchModel] = useJsonPatchCallback({});

  react.useEffect(() => saveUpdateHook(patchModel), [patchModel]);

  return html`
    <${LayoutContext.Provider} value=${{ sendEvent, loadImportSource }}>
      <${Element} model=${model} />
    <//>
  `;
}

function Element({ model }) {
  if (!model.tagName) {
    if (model.error) {
      return html`<pre>${model.error}</pre>`;
    } else {
      return null;
    }
  } else if (model.importSource) {
    return html`<${ImportedElement} model=${model} />`;
  } else {
    return html`<${StandardElement} model=${model} />`;
  }
}

function StandardElement({ model }) {
  const layoutContext = react.useContext(LayoutContext);
  // Use createElement here to avoid warning about variable numbers of children not
  // having keys. Warning about this must now be the responsibility of the server
  // providing the models instead of the client rendering them.
  return react.createElement(
    model.tagName,
    createElementAttributes(model, layoutContext.sendEvent),
    ...createElementChildren(
      model,
      (model) => html`<${Element} key=${model.key} model=${model} />`
    )
  );
}

function ImportedElement({ model }) {
  const layoutContext = react.useContext(LayoutContext);

  const importSourceFallback = model.importSource.fallback;
  const [importSource, setImportSource] = react.useState(null);

  if (!importSource) {
    // load the import source in the background
    loadModelImportSource(layoutContext, model.importSource).then(
      setImportSource
    );

    // display a fallback if one was given
    if (!importSourceFallback) {
      return html`<div />`;
    } else if (typeof importSourceFallback === "string") {
      return html`<div>${importSourceFallback}</div>`;
    } else {
      return html`<${StandardElement} model=${importSourceFallback} />`;
    }
  } else {
    return html`<${_ImportedElement}
      model=${model}
      importSource=${importSource}
    />`;
  }
}

function _ImportedElement({ model, importSource }) {
  const layoutContext = react.useContext(LayoutContext);
  const mountPoint = react.useRef(null);
  const sourceBinding = react.useRef(null);

  react.useEffect(() => {
    sourceBinding.current = importSource.bind(mountPoint.current);
    if (!importSource.data.unmountBeforeUpdate) {
      return sourceBinding.current.unmount;
    }
  }, []);

  // this effect must run every time in case the model has changed
  react.useEffect(() => {
    sourceBinding.current.render(model);
    if (importSource.data.unmountBeforeUpdate) {
      return sourceBinding.current.unmount;
    }
  });

  return html`<div ref=${mountPoint} />`;
}

function mountLayout(mountElement, layoutProps) {
  reactDom.render(react.createElement(Layout, layoutProps), mountElement);
}

function mountLayoutWithWebSocket(
  element,
  endpoint,
  loadImportSource,
  maxReconnectTimeout
) {
  mountLayoutWithReconnectingWebSocket(
    element,
    endpoint,
    loadImportSource,
    maxReconnectTimeout
  );
}

function mountLayoutWithReconnectingWebSocket(
  element,
  endpoint,
  loadImportSource,
  maxReconnectTimeout,
  mountState = {
    everMounted: false,
    reconnectAttempts: 0,
    reconnectTimeoutRange: 0,
  }
) {
  const socket = new WebSocket(endpoint);

  const updateHookPromise = new LazyPromise();

  socket.onopen = (event) => {
    console.info(`IDOM WebSocket connected.`);

    if (mountState.everMounted) {
      reactDom.unmountComponentAtNode(element);
    }
    _resetOpenMountState(mountState);

    mountLayout(element, {
      loadImportSource,
      saveUpdateHook: updateHookPromise.resolve,
      sendEvent: (event) => socket.send(JSON.stringify(event)),
    });
  };

  socket.onmessage = (event) => {
    const [pathPrefix, patch] = JSON.parse(event.data);
    updateHookPromise.promise.then((update) => update(pathPrefix, patch));
  };

  socket.onclose = (event) => {
    if (!maxReconnectTimeout) {
      console.info(`IDOM WebSocket connection lost.`);
      return;
    }

    const reconnectTimeout = _nextReconnectTimeout(
      maxReconnectTimeout,
      mountState
    );

    console.info(
      `IDOM WebSocket connection lost. Reconnecting in ${reconnectTimeout} seconds...`
    );

    setTimeout(function () {
      mountState.reconnectAttempts++;
      mountLayoutWithReconnectingWebSocket(
        element,
        endpoint,
        loadImportSource,
        maxReconnectTimeout,
        mountState
      );
    }, reconnectTimeout * 1000);
  };
}

function _resetOpenMountState(mountState) {
  mountState.everMounted = true;
  mountState.reconnectAttempts = 0;
  mountState.reconnectTimeoutRange = 0;
}

function _nextReconnectTimeout(maxReconnectTimeout, mountState) {
  const timeout =
    Math.floor(Math.random() * mountState.reconnectTimeoutRange) || 1;
  mountState.reconnectTimeoutRange =
    (mountState.reconnectTimeoutRange + 5) % maxReconnectTimeout;
  return timeout;
}

function LazyPromise() {
  this.promise = new Promise((resolve, reject) => {
    this.resolve = resolve;
    this.reject = reject;
  });
}

function mountWithLayoutServer(
  element,
  serverInfo,
  maxReconnectTimeout
) {
  const loadImportSource = (source, sourceType) =>
    import(sourceType == "NAME" ? serverInfo.path.module(source) : source);

  mountLayoutWithWebSocket(
    element,
    serverInfo.path.stream,
    loadImportSource,
    maxReconnectTimeout
  );
}

function LayoutServerInfo({ host, port, path, query, secure }) {
  const wsProtocol = "ws" + (secure ? "s" : "");
  const httpProtocol = "http" + (secure ? "s" : "");

  const uri = host + ":" + port;
  const url = (uri + path).split("/").slice(0, -1).join("/");

  const wsBaseUrl = wsProtocol + "://" + url;
  const httpBaseUrl = httpProtocol + "://" + url;

  this.path = {
    stream: wsBaseUrl + "/stream" + "?" + query,
    module: (source) => httpBaseUrl + `/modules/${source}`,
  };
}

export { LayoutServerInfo as L, mountWithLayoutServer as m };
