requirejs.config({
    paths: {
        /* Load cogram from CDN. */
        'cogram': [
            '//storage.googleapis.com/cogram-public/jupyter-cogram/latest/cogram_main.min',
        ],
    },
});

define(['cogram'], function (cogram,) {
    "use strict";
    const logPrefix = '[cogram-sources-loader]';
    console.log(logPrefix, "Loaded `cogram` module")
    return {
        load_jupyter_extension: cogram.load_jupyter_extension,
        load_ipython_extension: cogram.load_jupyter_extension
    };
});
