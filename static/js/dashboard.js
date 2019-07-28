$(function() {
    var file_div = $('.file_div');
    $('#dropzone-files').dropzone({
        parallelUploads: 2,
        maxFilesize:     50000,
        filesizeBase:    3000,
        addRemoveLinks:  true,
        success : function(file, response){
            console.log(file_div)
        }        
    });

    // Mock the file upload progress (only for the demo)
    //
Dropzone.options.myAwesomeDropzone = {
    maxFilesize: 5,
    addRemoveLinks: true,
    dictResponseError: 'Server not Configured',
  };

});