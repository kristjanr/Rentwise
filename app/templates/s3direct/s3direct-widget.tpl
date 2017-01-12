<div data-toggle="tooltip" title="These pictures will be displayed with your item. Upload pictures of your own item, not illustrative photos from Google." class="s3direct" data-policy-url="{{ policy_url }}">
  <a class="file-link" target="_blank" href="{{ file_url }}">{{ file_name }}</a>
  <a class="file-remove" href="#remove">Remove</a>
  <input class="file-url" type="hidden" value="{{ file_url }}" id="{{ element_id }}" name="{{ name }}" />
  <input class="file-dest" type="hidden" value="{{ dest }}">
  <input type="file" style="{{ style }}" class="file-input filestyle" data-classButton="btn btn-primary" data-input="false" data-classIcon="icon-plus" data-buttonText="Select image.">
  <div class="progress progress-striped active">
    <div class="bar"></div>
  </div>
</div>
