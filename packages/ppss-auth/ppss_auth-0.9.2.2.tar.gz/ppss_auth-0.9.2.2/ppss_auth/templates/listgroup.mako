<%inherit file="${context['midtpl']}" />

<table class="table">
	<thead>
		<tr>
			<th>${_('Group name')}</th>
			<th>${_('Permissions')}</th>
			<th>${_('Enabled')}</th>
			
			<th>${_('Action')}</th>
		</tr>
	</thead>
	<tbody>
		%for i,e in enumerate(elements):
			<tr>
				<td>${e.name}</td>
				<td>${", ".join([p.name for p in e.permissions])}</td>
				<td>${_("Yes") if e.enabled else _("No")}</td>
				<td>
					<a class="btn btn-success" href="${request.route_url('ppss:group:edit',elementid=e.id)}">${_('modify')}</a><br/>
				 </td>
			</tr>
		%endfor

	</tbody>


</table>

<div>
	<a class="btn btn-success" href="${request.route_url('ppss:group:edit',elementid = -1)}">${_('Add Group')}</a>
</div>