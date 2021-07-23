import {createObjectCsvStringifier} from 'csv-writer';

export function flattenJSON(json, exclude_empty_obj_arrays) {
  let result = {};

  // function to walk the json object
  function recurse(cur, prop) {
    if (Object(cur) !== cur) {
      result[prop] = cur;
    } else if (Array.isArray(cur)) {
      let l = cur.length;
      for (let i = 0; i < l; i++) recurse(cur[i], prop + "[" + i + "]");
      if (l === 0 && !exclude_empty_obj_arrays) result[prop] = [];
    } else {
      let isEmpty = true;
      for (let p in cur) {
        isEmpty = false;
        recurse(cur[p], prop ? prop + "." + p : p);
      }
      if (isEmpty && prop && !exclude_empty_obj_arrays) result[prop] = {};
    }
  }

  recurse(json, "");
  return result;
}

export function jsonToCSV(json) {
  // Create a unique set of column names for all included fields in the array of AHJs
  let flatJSON = flattenJSON(json, true);
  let keys = Object.keys(flatJSON);
  if (Array.isArray(json)) {
    keys = Array.from(new Set(keys.map(key => key.substring(key.indexOf('.') + 1))));
  } else {
    json = [json];
  }
  if (keys.length === 0) {
      return '';
  }
  const csvStringifier = createObjectCsvStringifier({ header: keys.map(key => { return {id: key, title: key }}) });
  let csv_rows = json.map(line => {
    return keys.reduce((result, key) => {
      result[key] = key.split(/[[\].]/)
          .filter(i => i !== '')
          .reduce((o, i) => Object.prototype.hasOwnProperty.call(o, i) ? o[i] : '', line);
      return result;
    }, {});
  });
  return csvStringifier.getHeaderString() + csvStringifier.stringifyRecords(csv_rows);
}
