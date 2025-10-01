// LEAF-Toolbox-SL2P
//     
/* GEE Javascript implementation of the   
   Simplified Level 2 Processor of Weiss and Baret (2016). 

 UPDATES:
 
 November 25, 202 - Updated code to  use Version 1 algorithms identical to LEAF Production at https://github.com/fqqlsun/LEAF_production/tree/main
 
 July 22, 2022 - Exported images now use projection of first image found.
 ap
 April 13,2021 - GEE dropped support for using bind when mapping functions over ee.List.sequence
                 Changed all such calls to use currying.  
                 Updated toolsNets  with curried functions.
                 The old version of code corresponds to April 12, 2021 if GEE decides to allow it again.  RF
                  

 Input: Collection of either Landsat 5 or Landsat 7 or Landsat 8 
        or Sentinel 2a or Sentinel 2b surface reflectance products.

        Imported EE asset with polygon features used to define spatial output region.
        By default only the first polygon is used.  However, you can change the feature number
        in the first line of the script.
        
        Links toEE assets networks and a land cover map using the
        North American Land Cover 2015 30m legend.
        http://www.cec.org/tools-and-resources/map-files/land-cover-30m-2015-landsat-and-rapideye
        
        By default the SL2P algorithm is implemented for supported collections.
        To use other algorithms comment out the SL2P algorithm assets below and 
        uncomment the desired algorithm ( e.g. CCRS) and run the code.

 Output: Unsigned int16 geotiff with layers
            1.  Estimate scaled by 1000
            2.  Standard error of estimates caled by 1000
            3.  Network number 
            4.  Quality control flags coded in binary flags
            5.  Land cover class
            6.  Days since January 1, 1970 inclusive
            
          One of the following quantities are estimated 
          Albedo: Black sky albedo at 10:30 local time.
          D:      Directional canopy scattering factor.
          fAPAR:  Fraction of absorbed photosynthetically active radiation, black sky at 10:30 local time.
          fCover: Fraction of canopy cover.
          LAI:    Leaf area index.
          CCC:    Canopy chlorophyll content.
          CWC:    Canopy water content.
.                                        */
          
/*--------------------------------------------------------------------------------*/
/*Start of user specification                                                     */
/*--------------------------------------------------------------------------------*/

/*--------------------------------------------------------------------------------*/
/* Region of interest , optional                                                  */
/*--------------------------------------------------------------------------------*/

var table = ee.FeatureCollection('projects/fast-blueprint-470916-f4/assets/ge1')
var featureNumber = ee.Number(0);
var geometry = ee.FeatureCollection(ee.Feature(table.toList(table.size()).get(featureNumber))).geometry();



//returns image with single band named networkid corresponding given 
// input partition image remapped to networkIDs

// applies a set of shallow networks to an image based on a provided partition image band
var wrapperNNets = function(network, partition, netOptions, colOptions, suffixName, imageInput){
  
  // typecast function parameters
  var network = ee.List(network);
  var partition = ee.Image(partition);
  var netOptions = netOptions;
  var colOptions = colOptions;
  var suffixName = suffixName;
  var imageInput = ee.Image(imageInput);

  // parse partition  used to identify network to use
  partition = partition.clip(imageInput.geometry()).select(['partition']);


  // determine networks based on collection
  var netList = ee.List(network.get(ee.Number(netOptions.variable).subtract(1))); 

  // parse land cover into network index and add to input image
  imageInput = imageInput.addBands(app.Nets.makeIndexLayer(partition,colOptions.legend,colOptions.Network_Ind));

  // define list of input names
  return(ee.ImageCollection(ee.List.sequence(0, netList.size().subtract(1))
                                                    .map(app.Nets.selectNet2(imageInput,netList,netOptions.inputBands))
                                                    .map(app.Nets.applyNet2(suffixName+app.vis.select.getValue())))
                                .max()
                  .addBands(partition))
                  .addBands(imageInput.select('networkID'));
                                

};

/*--------------------------------------------------------------------------------*/
/* Start of Helper functions                                                      */
/*--------------------------------------------------------------------------------*/

// convert number to string for mapping onto list
var toString = function(number) {
  return(ee.String(number));
};

/*--------------------------------------------------------------------------------*/
/* End  of Helper functions                                                      */
/*--------------------------------------------------------------------------------*/


// The namespace for our application.  All the state is kept in here.
var app = {};



// Applies the selection filters currently selected in the UI. 
app.applyFilters = function() {
  // set message we are loading images
  app.setLoadingMode(true);
        
  // Set filter variables.
  //Change to only take the first in the collection for debugging
  var start = app.filters.startDate.getValue();
  var end = app.filters.endDate.getValue();
  var colOptions = app.COLLECTION_OPTIONS[app.collectionName];
  var filtered = ee.ImageCollection(colOptions.name)
                   .filterBounds(app.filters.mapBounds)
                   .filterDate(start[1], end[1])
                   .filterMetadata(colOptions.Cloudcover,'less_than',app.filters.maxCloudcover.getValue())
                   .filterMetadata(colOptions.Watercover,'less_than',ee.Number(100))
                   .limit(5000);

  // Display how many granules were found 
  print('Found product granules');
  print(filtered);

  // Get the list of computed ids.
  var computedIds = filtered.limit(app.IMAGE_COUNT_LIMIT)
                            .reduceColumns(ee.Reducer.toList(), ['system:index'])
                            .get('list');

  // updathe the UI and proceed only if we get products
  computedIds.evaluate(function(ids) {
    // Update the image picker with the given list of ids.
    app.setLoadingMode(false);
    app.picker.select.items().reset(ids);
    
    // Default the image picker to the first id.
    app.picker.select.setValue(app.picker.select.items().get(0));
    
    // Disable the all images checbox
    app.picker.allImages.setValue(false);
  });
  
    // Refresh the map layer.
  app.refreshMapLayer();
};



// Export Collection of imaages to Google Drive
var ExportCol = function(col, folder, scale, projectionBand, type, nimg, maxPixels) {
  type = type || "float";
  nimg = nimg || 100;
  scale = scale || 20;
  maxPixels = maxPixels || 1e10;
  
  var colList = col.toList(nimg);
  var n = colList.size().getInfo();
  for (var i = 0; i < n; i++) {

    // restrict image to map bounds
    var img = ee.Image(colList.get(i)); //
    var imgBounds = app.filters.mapBounds.intersection(img.geometry(),10) ;
    // determine fi there are any valid values by checking for a null return om a reduces
    if ( img.select('timestart').reduceRegion({ reducer: ee.Reducer.max(), geometry: imgBounds, scale: 100}) !== null) {
      print('exporting')
      var id = img.id().getInfo() + "_" + app.vis.select.getValue();
   
      // set up type conversions
      var imgtype = {"float":img.toFloat(),  
                     "byte":img.toByte(), 
                     "unsigned int8":img.toByte(),
                     "unsigned int16":img.toUint16(),
                     "int":img.toInt(),
                     "double":img.toDouble(),
                     "unsigned int32":img.toUint32()
                    };

      // export image for map bounds only using desired type
      var projection = img.select(ee.List(projectionBand)).projection().getInfo();
      Export.image.toDrive({
        image:imgtype[type],
        description: id,
        folder: app.folder[0],
        fileNamePrefix: id,
        scale: scale,
        crs:projection.crs,
        crsTransform:projection.transform,
        region: imgBounds,
        maxPixels: app.pixels[0]});
  }
  }
};
  

  
  
// Exports  Products to Drive
app.exportMapLayer = function() {

  print('in export')
  // subset collection to one image if required
  var colOptions = app.COLLECTION_OPTIONS[app.collectionName];
  var netOptions = app.VIS_OPTIONS[app.vis.select.getValue()][app.filters.selectCollection.getValue()];
  var start = app.filters.startDate.getValue();
  var end = app.filters.endDate.getValue();
  var midDate = ee.Number(start[0]).add(ee.Number(end[0])).divide(2);
  if (app.picker.allImages.getValue()) {
    // filter collection for all products 
    var filtered =  ee.ImageCollection(colOptions.name)
                      .filterBounds(app.filters.mapBounds)
                      .filterDate(start[0], end[0])
                      .filterMetadata(colOptions.Cloudcover,'less_than',app.filters.maxCloudcover.getValue())
                      .limit(5000)
                      .map(app.Utils.addDate)
                      .map(function(image){return image.clip(app.filters.mapBounds)})
                      .map(app.Utils.deltaTime.bind(null,midDate))
                      .sort('deltaTime');
    }
  else {
    // process selected image only 
    var filtered =  ee.ImageCollection(app.filters.selectCollection.getValue())
                      .filter(ee.Filter.eq('system:index',app.picker.select.getValue()))
                      .map(app.Utils.addDate)
                      .map(function(image){return image.clip(app.filters.mapBounds)})
                      .map(app.Utils.deltaTime.bind(null,midDate))
                      .sort('deltaTime');
    }
    print('filtered')
    print(filtered)
    // mask based on collection, add score fo quality mosaicing and angles
    filtered = filtered.map(colOptions.tools.MaskClear)
                        .map(colOptions.tools.addSpecScore.bind(null,midDate))
                        .map(colOptions.tools.addGeometry.bind(null,colOptions));
 

    // process based on parameter value
    switch (app.vis.select.getValue()) {
      case 'Surface_Reflectance':
      
        print('starting exports')
        // Export data
        switch(app.exportID){
          case 'Image by Image':
            var export_image = ExportCol(filtered, 'Image_Export', colOptions.exportRes,[(filtered.first().bandNames().get(0))],"unsigned int16",100);
          break;
          case 'Full Map Mosaic':
            var projection = filtered.first().select(ee.List([(filtered.first().bandNames().get(0))])).projection().getInfo();
            filtered = filtered.qualityMosaic('spec_score');
            filtered = filtered.clip(app.filters.mapBounds.intersection(filtered.geometry(),10));
            var mosaicName = "mosaic"
            Export.image.toDrive({
                 image:  filtered.toUint16(),
                 description:mosaicName+ "_" + start[0] + "_" + end[0] + "_" + app.vis.select.getValue(),
                 folder: app.folder[0],
                 crs: projection.crs,
                 crsTransform: projection.transform,
                 scale:colOptions.exportRes,
                 maxPixels: app.pixels[0],
             });
  
          break;
          default: print('Invalid choice');
          break;
        }
      break;
      default:
      
      // mask non land vegetated areas
      filtered = filtered.map(colOptions.tools.MaskLand);
     
      
        //apply regression to estimate parameter
        print('starting sl2p')
        var partition = colOptions.partition.filterBounds(app.filters.mapBounds).mosaic().clip(app.filters.mapBounds).rename('partition');
        var scaledFiltered = filtered.map(app.Utils.scaleBands.bind(null,netOptions.inputBands,netOptions.inputScaling,netOptions.inputOffset))
                            .map(app.Nets.invalidInput.bind(null,colOptions.sl2pDomain,netOptions.inputBands))
        //print(scaledFiltered)
        var estimateSL2P = scaledFiltered.map(wrapperNNets.bind(null,app.SL2P,partition, netOptions, colOptions,'estimate')).map( function (image) { return image.select(['estimate'+netOptions.Name]).multiply(1000).addBands(image.select(['networkID','partition']))})
        //print(estimateSL2P)
        var uncertaintySL2P = scaledFiltered.map(wrapperNNets.bind(null,app.errorsSL2P,partition, netOptions, colOptions,'error')).map( function (image) { return image.select(['error'+netOptions.Name]).multiply(1000).addBands(image.select(['networkID','partition']))})
        //print(uncertaintySL2P);
        print('done sl2p') 
        
        print('starting exports')
        // Export data
        switch(app.exportID){
          case 'Image by Image':
            var export_image = ExportCol(scaledFiltered.select(['date','QC','spec_score']).combine(estimateSL2P).combine(uncertaintySL2P), 'Image_Export', colOptions.exportRes,['QC'],"unsigned int16",100);
          break;
          case 'Full Map Mosaic':
            var mosaicBounds = app.filters.mapBounds.intersection(scaledFiltered.qualityMosaic('spec_score').geometry(),10);
            scaledFiltered = scaledFiltered.select(['date','QC','spec_score']).combine(estimateSL2P).combine(uncertaintySL2P);
            var projection = scaledFiltered.first().select(['QC']).projection().getInfo();
            scaledFiltered = scaledFiltered.qualityMosaic('spec_score').clip(mosaicBounds).select(['date','QC','estimate'+netOptions.Name,'error'+netOptions.Name,'networkID','partition']);
            var mosaicName = "mosaic"
            Export.image.toDrive({
                 image:  scaledFiltered.toUint16(),
                 description:mosaicName+ "_" + start[0] + "_" + end[0] + "_" + app.vis.select.getValue(),
                 folder: app.folder[0],
                 crs: projection.crs,
                 crsTransform: projection.transform,
                 scale:colOptions.exportRes,
                 maxPixels: app.pixels[0],
             });
          break;
          default: print('Invalid choice');
          break;
        }
    break;
    }
    

};

/** Refreshes the current map layer based on the UI widget states. */
app.refreshMapLayer = function() {
  // clear map
  Map.clear();
  var colOptions = app.COLLECTION_OPTIONS[app.collectionName];
  var netOptions = app.VIS_OPTIONS[app.vis.select.getValue()][app.filters.selectCollection.getValue()];
  // print("colOptions", colOptions);
  //print("netOptions",netOptions);
  
  // subset collection to one image if required
  if (app.picker.select.getValue()) {
    var start = app.filters.startDate.getValue();
    var end = app.filters.endDate.getValue();
    var midDate = ee.Number(start[0]).add(ee.Number(end[0])).divide(2);
    if (app.picker.allImages.getValue()) {
      // filter collection for all products 
      var filtered =  ee.ImageCollection(colOptions.name)
                    .filterBounds(app.filters.mapBounds)
                    .filterDate(start[0], end[0])
                    .filterMetadata(colOptions.Cloudcover,'less_than',app.filters.maxCloudcover.getValue())
                    .limit(5000)
                    .map(app.Utils.addDate)
                    .map(function(image){return image.clip(app.filters.mapBounds)})
                    .map(app.Utils.deltaTime.bind(null,midDate))
                    .sort('deltaTime');
  
    }
    else {
      // process selected image only 
      var filtered =  ee.ImageCollection(colOptions.name)
                    .filter(ee.Filter.eq('system:index',app.picker.select.getValue()))
                    .map(app.Utils.addDate)
                    .map(function(image){return image.clip(app.filters.mapBounds)})
                    .map(app.Utils.deltaTime.bind(null,midDate))
                    .sort('deltaTime');
  
    }
    print('filtered')
    Map.addLayer(filtered)
    // mask based on collection, add score fo quality mosaicing and angles
    filtered = filtered.map(colOptions.tools.MaskClear)
                        .map(colOptions.tools.addSpecScore.bind(null,midDate))
                        .map(colOptions.tools.addGeometry.bind(null,colOptions))   
    Map.addLayer(filtered)

    // display based on parameter value
    switch (app.vis.select.getValue()) {
      case 'Surface_Reflectance':
        // Just show a RgB composite
       filtered  = filtered.qualityMosaic('spec_score');
        Map.clear()
        Map.addLayer(filtered, { bands:'date'},'Date');
        Map.addLayer(filtered,  colOptions.visParams  , 'Surface_Reflectance');
      break;
      default:
      
    // mask non land vegetated areas
      filtered = filtered.map(colOptions.tools.MaskLand);


      //apply regression to estimate parameter
      print('starting sl2p')
      var partition = colOptions.partition.filterBounds(app.filters.mapBounds).mosaic().clip(app.filters.mapBounds).rename('partition');
      var scaledFiltered = filtered.map(app.Utils.scaleBands.bind(null,netOptions.inputBands,netOptions.inputScaling,netOptions.inputOffset))
                          .map(app.Nets.invalidInput.bind(null,colOptions.sl2pDomain,netOptions.inputBands))
      var estimateSL2P = scaledFiltered.map(wrapperNNets.bind(null,app.SL2P,partition, netOptions, colOptions,'estimate'))
      //var estimateSL2P = ee.ImageCollection(wrapperNNets(app.SL2P,partition, netOptions, colOptions,'estimate',scaledFiltered.first()))
      //print(estimateSL2P)
      var uncertaintySL2P = scaledFiltered.map(wrapperNNets.bind(null,app.errorsSL2P,partition, netOptions, colOptions,'error'))
      //var uncertaintySL2P = ee.ImageCollection(wrapperNNets(app.errorsSL2P,partition, netOptions, colOptions,'error',scaledFiltered.first()))
      //print(uncertaintySL2P);
      
      // Mosaic after processing each product
      var mosaicResult = scaledFiltered.select(['date','QC','spec_score']).combine(estimateSL2P).combine(uncertaintySL2P).qualityMosaic('spec_score').clip(app.filters.mapBounds).select(['date','QC','estimate'+netOptions.Name,'error'+netOptions.Name,'networkID','partition']);
      //print(mosaicResult)
      print('done sl2p')

      //Displays the Collection of filtered images with the vis parameters 
      var visParams = app.VIS_OPTIONS[app.vis.select.getValue()][app.filters.selectCollection.getValue()]['outputParams'];
      var errorParams = app.VIS_OPTIONS[app.vis.select.getValue()][app.filters.selectCollection.getValue()]['errorParams'];
      Map.clear()
      Map.addLayer(scaledFiltered.first(),{},'input')
      Map.addLayer(mosaicResult, {bands:('partition'),min:0, max:20, palette:app.partitionPalettes.partitions.NALCMS[20]},'Partition');
      Map.addLayer(mosaicResult, { bands:'date'},'Date');
      Map.addLayer(mosaicResult, { bands:'QC'},'Quality Code'); 
      Map.addLayer(mosaicResult, {bands:('networkID'),min:0, max:20, palette:app.partitionPalettes.partitions.NALCMS[20]},'Network');
      Map.addLayer(mosaicResult, errorParams , netOptions.errorName);
      Map.addLayer(mosaicResult, visParams , netOptions.Name);

    break;
    }
  }
}

//  Creates the UI panels. 
app.createPanels = function() {
  // The introduction section. 
  app.intro = {
    panel: ui.Panel([
      ui.Label({
        value: 'LEAF Toolbox',
        style: {fontWeight: 'bold', fontSize: '24px', margin: '10px 5px'}
      }),
      ui.Label('This app allows you to display and export maps of  ' +
               'vegetation biophysical variables derived from the Sentinel 2 Multispectral Imager ' + 
               'or Landsat Imagers .')
    ])
  };


  // The collection filter controls. 
  app.filters = {
    // Create a select with a function that reacts to the "change" event.
    selectCollection: ui.Select({
      items: Object.keys(app.COLLECTION_OPTIONS),
      onChange: function(value) {
        app.collectionName = value;      
        var numNets = ee.Number(ee.Feature(app.COLLECTION_OPTIONS[app.collectionName].Network_Ind.first()).propertyNames().remove('Feature Index').remove('system:index').remove('lon').size());

        // changed from bind to currying RF April 15, 2021
        app.SL2P = ee.List.sequence(1,ee.Number(app.COLLECTION_OPTIONS[value].numVariables),1).map(app.Nets.makeNetVars2(app.COLLECTION_OPTIONS[app.collectionName].Collection_SL2P,numNets));
        app.errorsSL2P = ee.List.sequence(1,ee.Number(app.COLLECTION_OPTIONS[value].numVariables),1).map(app.Nets.makeNetVars2(app.COLLECTION_OPTIONS[app.collectionName].Collection_SL2Perrors,numNets));
      }
    }),
    startDate: ui.DateSlider({start: '1985-04-01',value:[(ui.DateSlider()).getEnd()-1000*3600*24*30,(ui.DateSlider()).getEnd()-1000*3600*24*30]}),
    endDate: ui.DateSlider({start:  '1985-04-01'}),
    maxCloudcover: ui.Slider({min: 0,max: 100,step:10}).setValue(90),
    selectminLng: ui.Textbox({
        placeholder:'min Long', 
        onChange:function(value){
          app.filters.selectBoundingBox.setValue(false);
          app.minLng = value; 
          return(value)}
    }),
    selectminLat: ui.Textbox({
        placeholder:'min Lat',
        onChange:function(value){
          app.filters.selectBoundingBox.setValue(false);
          app.minLat = value; 
          return(value)}
    }),
    selectmaxLng: ui.Textbox({
        placeholder:'max Long', 
        onChange:function(value){
          app.filters.selectBoundingBox.setValue(false);
          app.maxLng = value;
          return(value)}
    }),
    selectmaxLat: ui.Textbox({
        placeholder:'max Lat', 
        onChange:function(value){
          app.filters.selectBoundingBox.setValue(false);
          app.maxLat = value; 
          return(value);}
    }),
    selectBoundingBox: ui.Checkbox({
      label: "Use bounding box for ROI",
      onChange: function() {
        app.filters.mapBounds = ee.Geometry(Map.getBounds(true));
        if (app.filters.selectBoundingBox.getValue() === true) {
          app.filters.selectGeometry.setValue(false);
          var geo= ee.Geometry.Rectangle(ee.Number.parse(app.minLng), ee.Number.parse(app.minLat), ee.Number.parse(app.maxLng), ee.Number.parse(app.maxLat));
          app.filters.mapBounds = geo;
          Map.centerObject(geo);
        }
        //app.refreshMapLayer;
      }
    }),
    selectGeometry: ui.Checkbox({
      label: "Use geometry for ROI",
      onChange: function() {
        app.filters.mapBounds = ee.Geometry(Map.getBounds(true));
        if (app.filters.selectGeometry.getValue() === true) {
          app.filters.selectBoundingBox.setValue(false);
          var geo = geometry;
          app.filters.mapBounds = geo;
          Map.centerObject(geo);
        }
        //app.refreshMapLayer;
      }
    }),
    applyButton: ui.Button('Apply filters', app.applyFilters),
    loadingLabel: ui.Label({
      value: 'Loading...',
      style: {stretch: 'vertical', color: 'gray', shown: false}
    })
  };

    
  
  // Default the selectCollection to the first value.
  app.filters.selectCollection.setValue(app.filters.selectCollection.items().get(0));

  // Default bounds to current map bounds.
  app.filters.mapBounds = ee.Geometry(Map.getBounds(true));
    
  // The panel for the filter control widgets.
  app.filters.panel = ui.Panel({
    widgets: [
      ui.Label('1) Select filters', {fontWeight: 'bold'}),
      ui.Label('Collection', app.HELPER_TEXT_STYLE), app.filters.selectCollection,
      ui.Label('Start date', app.HELPER_TEXT_STYLE), app.filters.startDate,
      ui.Label('End date', app.HELPER_TEXT_STYLE), app.filters.endDate,
      ui.Label('Maximum cloud cover', app.HELPER_TEXT_STYLE), app.filters.maxCloudcover,
      app.filters.selectminLng,
      app.filters.selectminLat,
      app.filters.selectmaxLng,
      app.filters.selectmaxLat,
      app.filters.selectBoundingBox,
      app.filters.selectGeometry,
      ui.Panel([
        app.filters.applyButton,
        app.filters.loadingLabel
      ], ui.Panel.Layout.flow('horizontal'))
    ],
    style: app.SECTION_STYLE
  });

  // The product picker section. 
  app.picker = {
    // Create a select with a function that reacts to the "change" event.
    allImages: ui.Checkbox(
      {label: 'Process all products', value: false,
        onChange: app.refreshMapLayer
      }),
    select: ui.Select({
      placeholder: 'Select product',
      onChange: app.refreshMapLayer
    })
  };

  // The panel for the picker section with corresponding widgets. 
  app.picker.panel = ui.Panel({
    widgets: [
      ui.Label('2) Select products', {fontWeight: 'bold'}),
      ui.Panel([
        app.picker.select,
      ], ui.Panel.Layout.flow('horizontal')),
      app.picker.allImages,
    ],
    style: app.SECTION_STYLE
  });


// The visualization section. 
  app.vis = {
    label: ui.Label(),
    // Create a select with a function that reacts to the "change" event.
    select: ui.Select({
      items: Object.keys(app.VIS_OPTIONS),
      //items: Object.keys(app.COLLECTION_OPTIONS[app.filters.selectCollection.getValue()].VIS_OPTIONS),
      onChange: function() {
        // Update the label's value with the select's description.
        var option = app.VIS_OPTIONS[app.vis.select.getValue()];
        app.vis.label.setValue(option.description);
        // Refresh the map layer.
        app.refreshMapLayer();
      }
    })
  }; 

  // The panel for the visualisation section with corresponding widgets. 
  app.vis.panel = ui.Panel({
    widgets: [
      ui.Label('3) Select a variable to display', {fontWeight: 'bold'}),
      app.vis.select,
      app.vis.label
    ],
    style: app.SECTION_STYLE
  }); 
  app.vis.select.setValue(app.vis.select.items().get(0));
  

  // The export section. 
  app.export = {
    label: ui.Label(),
    // Create a select with a function that reacts to the "change" event.
    select: ui.Select({
      items: Object.keys(app.EXP_OPTIONS),
      
        // Update the label's value with the select's description.
        onChange: function(value){
      
        app.exportID = value; 
        } 
    }),
       textbox1: ui.Textbox({
        placeholder:'Enter folder name',
        
        onChange: function(text){
          app.folder = [''];
          app.folder[0] =  app.export.textbox1.getValue();
          print('Into Folder:', app.folder[0]);
        }
      }),
        textbox2: ui.Textbox({
        placeholder:'Enter Max Pixels',
        
        onChange: function(text){
          app.pixels = [0];
          app.pixels[0] = app.export.textbox2.getValue();
          print('Max Pixels:', app.pixels[0]);
        }
      }),
    exportButton: ui.Button({
      label:'Apply Export',  
      
      onClick: function(){
        
        app.exportMapLayer();
       }
      })
  };

  // The panel for the export section with corresponding widgets. 
  app.export.panel = ui.Panel({
    widgets: [
      ui.Label('4) Exporting Results to Drive', {fontWeight: 'bold'}),
      app.export.select,
      app.export.label,
      app.export.textbox1,
      app.export.textbox2,
      app.export.exportButton
    ],
    style: app.SECTION_STYLE
  });

   app.export.select.setValue(app.export.select.items().get(0));
};


// Creates the app helper functions. 
app.createHelpers = function() {
  /**
   * Enables or disables loading mode.
   * @param {boolean} enabled Whether loading mode is enabled.
   */
  app.setLoadingMode = function(enabled) {
    // Set the loading label visibility to the enabled mode.
    app.filters.loadingLabel.style().set('shown', enabled);
    // Set each of the widgets to the given enabled mode.
    var loadDependentWidgets = [
      app.vis.select,
      app.filters.startDate,
      app.filters.endDate,
      app.filters.maxCloudcover,
      app.filters.selectminLng,
      app.filters.selectminLat,
      app.filters.selectmaxLng,
      app.filters.selectmaxLat,
      app.filters.selectBoundingBox,
      app.filters.selectGeometry,
      app.filters.applyButton,
      app.export.exportButton
    ];
    loadDependentWidgets.forEach(function(widget) {
      widget.setDisabled(enabled);
    });
  };
};


// Creates the app constants. 
app.createConstants = function() {
  
  // palettes for display
  // generic palette
  // palettes for parition layer, should be deprecated
  app.partitionPalettes = require('users/rfernand387/exports:partitionPalettes');
  app.partitionMin = ee.Number(0);
  app.partitionMax = ee.Number(20);
 
  
    // load modules
  app.fc = require('users/rfernand387/LEAFToolboxModules:feature-collections-SL2P');
  app.dictionariesSL2P = require('users/rfernand387/LEAFToolboxModules:dictionaries-SL2P'); 
  app.batch = require('users/fitoprincipe/geetools:batch');
  app.Utils = require('users/rfernand387/LEAFToolboxModules:toolsUtils');
  app.Nets = require('users/rfernand387/LEAFToolboxModules:toolsNets');
  app.NOW = Date.Now; 
  app.COLLECTION_ID = 'COPERNICUS/S2';
  app.SECTION_STYLE = {margin: '20px 0 0 0'};
  app.HELPER_TEXT_STYLE = {
      margin: '8px 0 -3px 8px',
      fontSize: '12px',
      color: 'gray'
  };
  app.IMAGE_COUNT_LIMIT = 100;
  app.EXP_OPTIONS = {'Image by Image':{Order :1},
                     'Full Map Mosaic':{Order: 2}};

 app.COLLECTION_OPTIONS = app.dictionariesSL2P.make_collection_options(app.fc);
 app.VIS_OPTIONS = app.dictionariesSL2P.make_net_options();

  
};



// Creates the application interface
app.boot = function() {

  app.createConstants();
  app.createHelpers();
  app.createPanels();
  var main = ui.Panel({
    widgets: [
      app.intro.panel,
      app.filters.panel,
      app.picker.panel,
      app.vis.panel,
      app.export.panel
    ],
    style: {width: '320px', padding: '8px'}
  });
  ui.root.insert(0, main);
  

  
};


// Start app
app.boot(); 