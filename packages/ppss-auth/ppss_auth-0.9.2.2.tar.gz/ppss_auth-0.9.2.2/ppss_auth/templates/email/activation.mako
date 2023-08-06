<html>
<body>
  <% activationurl = request.route_url('activate',_params={'magicnumber':magicnumber}) %>
  _("Hello") ${username},<br/>
  <p>
  please click <a href="${activationurl}">here</a> to activate your account or visit the link below:
  </p>
  <p>
    <a href="${activationurl}">${activationurl}</a>
  </p>
</body></html>