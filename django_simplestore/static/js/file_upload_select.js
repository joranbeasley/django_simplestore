function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = grp.jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

var d=grp.jQuery('<div id="dialog" title="Upload File">')
var f=grp.jQuery('<form action="/admin/upload_file?next='+document.location.href+'" method="post" enctype="multipart/form-data">')
var l=grp.jQuery('<label>').text("File Upload").append('<br>')
var inp = grp.jQuery('<input type="file" name="joran_file">')
var submit_btn = grp.jQuery('<input type="submit" value="Upload File">')

d.append(f)
f.append(l).append('<br>').append(inp).append('<br>').append('<input type="hidden" name="csrfmiddlewaretoken" value="'+csrftoken+'">').append(submit_btn)

grp.jQuery(document).ready(function() {
    var opt = grp.jQuery("<option>")
    opt.text("Upload new image...")
    grp.jQuery(".file-select select").append(opt)
    grp.jQuery(document).on('change', 'select', function() {
        if(grp.jQuery(this).val() == "Upload new image...") { // the selected options’s value
            d.dialog({modal:true})
        }
    });
});