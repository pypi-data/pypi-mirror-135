<%inherit file="${context['midtpl']}" />

<div class="row">
    <div class="${bc['xs']}12">
        <form class="form" action="${request.route_url('ppss:group:edit',elementid=groupid)}" method="POST">
            <input type="hidden" value="${get_csrf_token()}" name="csrf_token">
            <div class="form-group">
            <input class="form-control" type="text" name="name" placeholder="group name" value="${group.name if group else ""}">
            </div>
            <div class="checkbox">
                <label for="enablecheck">${_('Enable group:')}</label>
                <input id="enablecheck" name="enablecheck" type="checkbox" value="1" ${'checked="checked"' if group.enabled else ""}>
            </div>
            <div>
                <input class="btn btn-success" type="submit" name="submit" value="${_('Apply')}"/>
                <a class="btn btn-danger" href="${request.route_url('ppss:perm:delete',elementid=group.id)}">${_('remove group')}</a>
            </div>
            <p>${msg}</p>
        </form>
    </div>
    <div class="${bc['xs']}12">
        <div class="row">
            <div class="col-12 col-sm-6">
                    <h3>${_('User to remove')}</h3>            
                    <ul class="list-group" data-userdelete>
                    </ul>
            </div>
            <div class="${bc['xs']}12 col-sm-6">
                    <h3>${_('User to add')}</h3>
                    <input type="text" data-user-autocomplete class="form-control" />
                    </br>
                    <ul class="list-group" data-useradd>
                    </ul>
            </div>
        </div>
    </div>
    <div class="${bc['xs']}12">
        <div class="row">
            <div class="${bc['xs']}12 col-sm-6">
                    <h3>${_('Perm to remove')}</h3>
                    <ul class="list-group" data-permdelete>
                    </ul>
            </div>
            <div class="${bc['xs']}12 col-sm-6">
                    <h3>${_('Perm to add')}</h3>
                    <ul class="list-group" data-permadd>
                    </ul>
            </div>
        </div>
    </div>
</div><!-- .row -->
<script src="https://ajax.googleapis.com/ajax/libs/jqueryui/1.12.1/jquery-ui.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/handlebars.js/4.0.11/handlebars.min.js"></script>
<script src="${request.static_url('ppss_auth:ppss_auth_static/loader.js')}"></script>
<script type="text/javascript">
        var currentPermissions = [
            %for p in group.permissions:
                {'id':${p.id},'name':"${p.name}"},
            %endfor
        ];

        var availablePermissions = [
            %for p in allperm:
                {'id':${p.id},'name':"${p.name}"},
            %endfor
        ];

        var currentUsers = [
            %for user in group.users:
                {'id':${user.id},'username':"${user.username}"},
            %endfor
        ];

        var allUsers = [
            %for user in users:
                {'id':${user.id},'username':"${user.username}"},
            %endfor
        ];

        var routes = {
            TEMPLATE: "${request.static_url('ppss_auth:ppss_auth_static/template.html')}",
            REMOVE_USER: "${request.route_url('ppss:group:removeuser',targetid=-1,elementid=group.id)}",
            ADD_USER: "${request.route_url('ppss:group:adduser',targetid=-1,elementid=group.id)}",
            REMOVE_PERM: "${request.route_url('ppss:group:removeperm',targetid=-1,elementid=group.id)}",
            ADD_PERM: "${request.route_url('ppss:group:addperm',targetid=-1,elementid=group.id)}",
            SEARCH_USER: "${request.route_url('ppss:user:search')}"
        }
</script>
<script src="${request.static_url('ppss_auth:ppss_auth_static/ppssauth.js')}"></script>