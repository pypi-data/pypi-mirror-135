<%inherit file="${context['logintpl']}" />
<div class="container">
  <div class="row text-center">
      <div class="${bc['xs']}12 col-md-4 offset-md-4">
        <form action="${request.route_url('ppss:user:changepassword')}" method="POST" class="ppssauthform">
            <input type="hidden" value="${get_csrf_token()}" name="csrf_token">
            <h2>${_("Change password for user {username}").format(username=request.loggeduser.username) }</h2>
            <input type="password" name="oldpassword" placeholder="${_('current password')}">
            <br/>
            <input type="password" name="newpassword" placeholder="${_('new password')}">
            <br/>
            <input type="password" name="confirmnewpassword" placeholder="${_('confirm new password')}">
            <br/>
            <div class="text-center">
              <input type="submit" name="submit" value="${_('update')}"/>
            </div>

            <p>${msg}</p>
        </form>
      </div>
  </div>
</div>
