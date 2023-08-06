/**
 * Module providing the ability to upload files from the local filesystem.
 */
let upload = function() {
    /**
     * Default configuration of this module.
     */
    let config = {
        fileSelect: "#ys-select-local-files",
        fileSelectForm: "form#ys-upload-form",
        progress: 'div#ys-progress',
    };

    let c = config;    // internal alias for brevity

    /**
     * Upload YANG files to the selected repository.
     */
    function uploadToRepo(repo) {
        if ($(c.fileSelect)[0].files.length == 0) {
            popDialog("Please select one or more files to upload");
            return;
        }

        $.ajaxSetup({
            beforeSend: function(xhr, settings) {
                if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", Cookies.get('csrftoken'));
                }
            }
        });

        let progress = $(c.progress);
        progress.progressbar({value: false});

        let data = new FormData();
        data.append('repository', repo);
        $.each($(c.fileSelect)[0].files, function(i, file) {
            data.append('files', file);
        });

        return $.ajax({
            url: "/filemanager/upload/to_repository/",
            data: data,
            type: 'POST',
            processData: false,
            contentType: false,
            success: function(retObj) {
                repository.getRepoContents(repo);
                progress.progressbar("destroy");
                repository.checkRepo(repo);
            },
            error: function(retObj) {
                progress.progressbar("destroy");
            },
        });
    };

    /* Public API */
    return {
        config:config,
        uploadToRepo:uploadToRepo,
    };
}();
