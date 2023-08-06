#!/usr/bin/env node

'use strict';

const constants = require('./const');
const path = require('path');
const fs = require('fs');
const generateReviewDocument = require('./payloadGenerator');
const resolveAllImagesAsBase64 = require('./utilities/image');
const resolveVideoFrames = require('./utilities/video');
const {
  generateYAMLJSON,
  copyProcedureAssets,
  downloadDocument,
  writeJSON,
  error,
  printHelp,
} = require('./utilities/io');

const args = require('minimist')(process.argv.slice(2), {
  boolean: ['help', 'dev', 'log', 'extract'],
  string: ['procedure', 'endpoint', 'output', 'input_json'],
});

const main = async () => {
  console.log(`Resolving assets...`);
  // check if there is input json and try to resolve it
  // if exist continue processing but skip generating and processing images/json
  let procedureWithImages;
  if (args.input_json && fs.existsSync(args.input_json)) {
    procedureWithImages = JSON.parse(fs.readFileSync(args.input_json));
  } else if (args.procedure) {
    const procedure = generateYAMLJSON(args.procedure);
    resolveVideoFrames(procedure, procedure.procedure_name);
    procedureWithImages = await resolveAllImagesAsBase64(
      procedure,
      procedure.procedure_name,
      args.extract
    );
  } else {
    error(`File at: ${args.input_json} cannot be resolved.`, true);
  }
  return Promise.all([procedureWithImages]).then(([procedureWithImgs]) => {
    args.log &&
      console.log(
        `Writing ${constants.devLogOutputPath}/${procedureWithImgs.procedure_name}.json...`
      );
    args.log &&
      writeJSON(
        `${constants.devLogOutputPath}/${procedureWithImgs.procedure_name}.json`,
        procedureWithImgs
      );
    console.log(`Generating payload...`);
    const payload = generateReviewDocument(
      procedureWithImgs,
      constants,
      args.extract
    );
    args.log &&
      console.log(
        `Writing ${constants.devLogOutputPath}/${procedureWithImgs.procedure_name}_payload.json...`
      );
    args.log &&
      writeJSON(
        `${constants.devLogOutputPath}/${procedureWithImgs.procedure_name}_payload.json`,
        payload
      );
    if (args.endpoint || args.dev) {
      const format = args.extract ? 'html' : 'pdf';
      const outputPath = args.output
        ? `${args.output}/${args.extract ? `${args.procedure}/` : ''}${
            procedureWithImgs.procedure_name
          }.${format}`
        : `${constants.defaultPdfOutputPath}/${
            args.extract ? `${args.procedure}/` : ''
          }${procedureWithImgs.procedure_name}.${format}`;
      if (args.extract) {
        const outputFolder = `${path.dirname(outputPath)}/procedure_assets`;
        console.log(`Copying procedure assets to: ${outputFolder}`);
        copyProcedureAssets(args.procedure, outputFolder);
      }
      if (args.endpoint) {
        console.log(`Posting payload to: ${args.endpoint}`);
        downloadDocument(JSON.stringify([payload]), args.endpoint, outputPath);
      }
      if (args.dev) {
        console.log(
          `Posting payload to local server at: ${constants.DEV_ENDPOINT}`
        );
        downloadDocument(
          JSON.stringify([payload]),
          constants.DEV_ENDPOINT,
          outputPath
        );
      }
    }
  });
};

if (args.help) {
  printHelp(true);
}

if (!args.procedure && !args.endpoint && !args.input_json) {
  error(
    'Incorrect usage. Procedure name, input data or endpoint must be provided.',
    true
  );
}

main();
