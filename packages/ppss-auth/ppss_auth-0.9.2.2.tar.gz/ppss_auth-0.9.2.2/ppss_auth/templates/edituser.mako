<%inherit file="${context['midtpl']}" />

<%
usergroups = {}
for g in user.groups:
    usergroups[g.id] = g.name
%>
<div class="row">
    <div class="${bc['xs']}12 col-sm-6">
        <form action="${submiturl}" method="POST" autocomplete="off">
            <input type="hidden" value="${get_csrf_token()}" name="csrf_token">
            <input type="hidden" name="userid" value="${user.id if (user and user.id) else '-1'}">
            <input class="form-control" type="text" name="username" placeholder="${_('username')}" value="${user.username if (user and user.username) else ''}">
            </br>
            %if selfediting or ((request.loggeduser.isSuperUser() == False) and user.id and user.id >= 0):
            <input class="form-control" type="password" name="currentpassword" placeholder="${_('current password')}" value="">
            </br>
            %endif
            <input class="form-control" type="password" name="password" placeholder="${_('password')}" value="" autocomplete="new-password">
            </br>
            <input class="form-control" type="password" name="confirmnewpassword" placeholder="${_('confirm new password')}" value="" autocomplete="new-password">
            <div class="checkbox">
                <label for="enablecheck">
                    <input id="enablecheck" type="checkbox" value="1" ${'checked="checked"' if user and user.enabled else ''} name="enabled"> ${_('Enable:')}
                </label>
            </div>
            <p class="label">${_('Groups')}</p>
            %for g in allgroups:
                <label class="checkbox-inline">
                    <input name="allgroups" type="checkbox" value="${g.id}" ${"checked" if g.id in usergroups else ""}> ${g.name}
                </label>
            %endfor
            </br>
            <input class="btn btn-success" type="submit" name="submit" value="${_('Apply')}"/>

            <p class="resultmsg">${msg}</p>
        </form>
    </div>
</div>