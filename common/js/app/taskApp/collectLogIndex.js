$(function() {
	$(".type").combobox({
		valueField: 'value',
		textField: 'text',
		data: [{
			"value": "1",
			"text": "普通文件本地上传"
		},
			{
			"value": "5",
			"text": "普通文件远程下载"
		},
			{
			"value": "2",
			"text": "数据库文件"
		}, {
			"value": "3",
			"text": "数据接口"
		}, {
			"value": "4",
			"text": "API接口"
		}],
	})

})

$(function(){
	$("#collectLogList").datagrid({
		url:'/collectLogIndex/collection/',
		autoRowHeight:true,
		singleSelect:true,
		columns:[[
			{field:'taskname',title:'任务名称',width:'20%',},
			{field:'starttime',title:'开始时间',width:'25%',},
			{field:'endtime',title:'结束时间',width:'25%',},
			{field:'state',title:'当前状态',width:'15%',
			formatter: function(value,row,index) {
				if (value == 1) {
					return '采集完毕';
				}
				else {
					return '正在采集'
				}
			}
			},
			{field:'oper',title:'查看任务详情',width:'12%',formatter:func},
		]],
		onLoadSuccess:function(){
			$('.collectDetail').linkbutton({
					iconCls: 'icon-more',
				});
		}
	})

function func(v,r,i){
	return '<a class="collectDetail" href="javascript:collectDetail();"  data-options="" style="margin:8px 5px;">详情</a>'

}
			 $('#runTaskSearchBox').searchbox({
        	prompt:'请输入任务名称搜索',
        	height:24,
        	width:200,
        	searcher:function(v,n){
           		$('#collectLogList').datagrid('load', {condition:v,type:1});
				console.log(v);
				console.log('111');
        }
    })
})



function collectDetail() {
		var data = $("#collectLogList").datagrid('getSelected');
	    var type = data.type
	    if (type=='1') {
			linkbutton_click('open_dialog', {dialog: '#fileUploadDetailDialog'});
			$.get('/sjyglIndex/taskInfo//', {data:data.taskid}, function (ret) {
				$(".type").combobox("select", ret[0].filetype); //获取数据到input框
				$("#fileTasName").val(ret[0].taskname);
				$("#filetaskId").val(ret[0].taskid);
				$("#fileBelong").val(ret[0].belongto);
				$("#fileBelType").val(ret[0].belongtype);
				$("#fileTaskdom").val(ret[0].domid);
				$("#sfileName").val(ret[1].filename);
				$("#sfileNameWay").val(ret[1].fileway);
				$("#saveTypeFile").val(ret[1].sfiletype);
			})
		}
	    if (type=='2') {
			linkbutton_click('open_dialog', {dialog: '#sqlDetailDialog'});
			$.get('/sjyglIndex/taskInfo/', {data: data.taskid}, function (ret) {
				  $(".type").combobox("select", ret[0].filetype);
				$("#sqlTasName").val(ret[0].taskname);
				$("#sqltaskId").val(ret[0].taskid);
				$("#sqlBelong").val(ret[0].belongto);
				$("#sqlBelType").val(ret[0].belongtype);
				$("#sqlTaskdom").val(ret[0].domid);
				$("#sqlfileName").val(ret[1].filename);
				$("#sqlfileNameWay").val(ret[1].fileway);
				$("#sqlsaveType").val(ret[1].tasktype);
			})
		}
	    if (type=='3') {
			linkbutton_click('open_dialog', {dialog: '#collectdetailDialog'});
			$.get('/sjyglIndex/taskInfo/', {data: data.taskid}, function (ret) {
				$(".type").combobox("select", ret[0].filetype);
				$("#taskName").val(ret[0].taskname);
				$("#taskId").val(ret[0].taskid);
				$("#belong").val(ret[0].belongto);
				$("#belType").val(ret[0].belongtype);
				$("#belongdoman").val(ret[0].domid);
				$("#dataSoure").val(ret[1].sjyname);
				$("#dbName").val(ret[1].databasename);
				$("#sqltype").val(ret[1].databasetype);
				$("#userName").val(ret[1].username);
				$("#password").val(ret[1].pwd);
				$("#connIp").val(ret[1].fwqadress);
				$("#port").val(ret[1].dkname);
				$("#table").val(ret[1].tablename);
				$("#fields").val(ret[1].ziduanname);
				$("#runtime").val(ret[0].refreshChange);
			})
		}
	    if (type=='4') {
			linkbutton_click('open_dialog', {dialog: '#apiDetailDialog'});
			$.get('/sjyglIndex/taskInfo/', {data: data.taskid}, function (ret) {
				$(".type").combobox("select", ret[0].filetype);
				$("#apiTasName").val(ret[0].taskname);
				$("#taskIdApi").val(ret[0].taskid);
				$("#apiBelong").val(ret[0].belongto);
				$("#apiBelType").val(ret[0].belongtype);
				$("#aTaskdom").val(ret[0].domid);
				$("#urlAd").val(ret[1].url);
				$("#useMethod").val(ret[1].apitype);
				$("#param").val(ret[1].param);
				$("#byteAmout").val(ret[1].byteamount);
				$("#saveType").val(ret[1].filetype);
			})
		}
	    if (type=='5') {
			linkbutton_click('open_dialog', {dialog: '#fileDownloadDetailDialog'});
			$.get('/sjyglIndex/taskInfo/', {data: data.taskid}, function (ret) {
				$(".type").combobox("select", ret[0].filetype);
				$("#downloadfileTasName").val(ret[0].taskname);
				$("#dowlfiletaskId").val(ret[0].taskid);
				$("#dowlfileBelong").val(ret[0].belongto);
				$("#dowlfileBelType").val(ret[0].belongtype);
				$("#dowlfileTaskdom").val(ret[0].domid);
				$("#dfileNameWay").val(ret[1].path);
				$("#downloadIp").val(ret[1].ip);
				$("#dUsername").val(ret[1].user);
				$("#downloadPwd").val(ret[1].pwd);
			})
		}
}

function sqlApiDialogClose() {
		$('#collectdetailDialog').dialog('close');
}


function apiDialogClose() {
		$('#apiDetailDialog').dialog('close');
}

function sqlDialogClose() {
		$('#sqlDetailDialog').dialog('close');
}















