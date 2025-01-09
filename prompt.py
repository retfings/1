from openai import OpenAI
import os
import pandas as pd
client = OpenAI(api_key="sk-c765e87a50df47cfb82b0c16c6da0066", base_url="https://api.deepseek.com")

# print(keys)
data_type_descriptions = {
    "Met": "测量数据（Metrology）",
    "Defect": "缺陷数据（Defect data）",
    "WS": "晶圆状态（Wafer Status）",
    "History": "历史数据（Historical data）",
    "FDC": "故障检测与分类（Fault Detection and Classification）",
    "WAT": "晶圆接受测试（Wafer Acceptance Test）",
    "Offline": "离线数据（Offline data）",
    "FT": "前段测试（Final Test）",
    "INK": "打标数据（Ink Marking）",
    "Downgrade": "降级数据（Downgrade data）",
    "Others": "其他数据（Other data）"
}



table_name_map = {
    "dws_met_inline_pam_wf": "在线参数工作流 (Inline Parameter Workflow)",
    "dwd_met_inline_dtl_v": "在线详细视图 (Inline Detail View)",
    "dws_met_offline_param_wf": "离线参数工作流 (Offline Parameter Workflow)",
    "dwd_met_offline_param_v": "离线参数视图 (Offline Parameter View)",
    "dws_defect_class_wf": "缺陷分类工作流 (Defect Classification Workflow)",
    "dwd_defect_chart_wafer": "缺陷图表晶圆 (Defect Chart Wafer)",
    "dwd_insp_defect_v": "缺陷检测视图 (Inspection Defect View)",
    "dwd_insp_wafer_summary_v": "晶圆检测汇总视图 (Wafer Inspection Summary View)",
    "dws_ws_hardbin_wf": "硬件绑定工作流 (Hardbin Workflow)",
    "dws_ws_hardbin_wd": "硬件绑定宽度 (Hardbin Width)",
    "dws_ws_param_wf": "参数工作流 (Parameter Workflow)",
    "dws_ws_bb_wf": "BB 工作流 (BB Workflow)",
    "dws_ws_ett_wf": "ETT 工作流 (ETT Workflow)",
    "dws_ws_funcbin_wf": "功能绑定工作流 (Function Bin Workflow)",
    "dws_ws_fwl_wf": "FWL 工作流 (FWL Workflow)",
    "dws_ws_fwl_die": "FWL 晶粒 (FWL Die)",
    "dws_ws_rdmargin_wf": "RD 裕度工作流 (RD Margin Workflow)",
    "dws_ws_pcollevel_wf": "PCol 级别工作流 (PCol Level Workflow)",
    "dwd_ws_hardbin_v": "硬件绑定视图 (Hardbin View)",
    "dwd_ws_param_die_v": "参数晶粒视图 (Parameter Die View)",
    "dwd_ws_bb_v": "BB 视图 (BB View)",
    "dwd_ws_bb_mark_v": "BB 标记视图 (BB Mark View)",
    "dwd_ws_pf_ett_v": "PF ETT 视图 (PF ETT View)",
    "dwd_ws_funcbin_v": "功能绑定视图 (Function Bin View)",
    "dwd_ws_vtdist_v": "VT 分布视图 (VT Distribution View)",
    "dwd_ws_vt_ivs_stat_v": "VT IVS 统计视图 (VT IVS Statistic View)",
    "dwd_ws_fwl_v": "FWL 视图 (FWL View)",
    "dwd_ws_rdmargin_v": "RD 裕度视图 (RD Margin View)",
    "dwd_ws_pcollevel_v": "PCol 级别视图 (PCol Level View)",
    "dwd_ws_leakage_x8_v": "泄漏 X8 视图 (Leakage X8 View)",
    "dwd_ws_grade_check_result": "等级检查结果 (Grade Check Result)",
    "dwd_ws_grade_check_result_detail": "等级检查结果详情 (Grade Check Result Detail)",
    "dwd_wip_weh_v": "在制品 WEH 视图 (WIP WEH View)",
    "dwd_wip_leh_v": "在制品 LEH 视图 (WIP LEH View)",
    "dwd_fdc_indicator_dtl_v": "FDC 指标详细视图 (FDC Indicator Detail View)",
    "dws_wat_param_wf": "WAT 参数工作流 (WAT Parameter Workflow)",
    "dwd_wat_param_v": "WAT 参数视图 (WAT Parameter View)",
    "dwd_ft_fab_wafer_info_prod_v": "FT 晶圆信息生产视图 (FT Wafer Info Production View)",
    "dwd_ft_lotinfo_prod_v": "FT 批次信息生产视图 (FT Lot Info Production View)",
    "dwd_ft_summary_yield_prod_v": "FT 产量汇总生产视图 (FT Yield Summary Production View)",
    "dwd_ft_summary_yield_mer_prod_v": "FT 合并产量汇总生产视图 (FT Merged Yield Summary Production View)",
    "dwd_ft_summary_hardbin_prod_v": "FT 硬件绑定汇总生产视图 (FT Hardbin Summary Production View)",
    "dwd_ft_summary_hardbin_mer_prod_v": "FT 合并硬件绑定汇总生产视图 (FT Merged Hardbin Summary Production View)",
    "dwd_ft_summary_softbin_prod_v": "FT 软件绑定汇总生产视图 (FT Softbin Summary Production View)",
    "dwd_ft_summary_softbin_mer_prod_v": "FT 合并软件绑定汇总生产视图 (FT Merged Softbin Summary Production View)",
    "dwd_ft_bin_dielevel_summary_prod_v": "FT 晶粒级绑定汇总生产视图 (FT Bin Dielevel Summary Production View)",
    "dwd_ft_bin_dutlevel_summary_prod_v": "FT DUT 级绑定汇总生产视图 (FT Bin DUT Level Summary Production View)",
    "dwd_ft_tt_sitelevel_summary_prod_v": "FT TT 站点级汇总生产视图 (FT TT Site Level Summary Production View)",
    "dwd_ft_parameters_dielevel_summary_prod_v": "FT 晶粒级参数汇总生产视图 (FT Parameters Dielevel Summary Production View)",
    "dwd_ft_parameters_dielevel_wafer_summary_prod_v": "FT 晶粒级晶圆汇总参数视图 (FT Parameters Dielevel Wafer Summary Production View)",
    "dwd_ft_parameters_dutlevel_summary_prod_v": "FT DUT 级参数汇总生产视图 (FT Parameters DUT Level Summary Production View)",
    "dwd_ft_bin_dielevel_rawdata_prod_v": "FT 晶粒级绑定原始数据视图 (FT Bin Dielevel Raw Data Production View)",
    "dwd_ft_bin_dutlevel_rawdata_prod_v": "FT DUT 级绑定原始数据视图 (FT Bin DUT Level Raw Data Production View)",
    "dwd_ft_tt_sitelevel_rawdata_prod_v": "FT TT 站点级原始数据视图 (FT TT Site Level Raw Data Production View)",
    "dwd_ft_parameters_dielevel_rawdata_prod_v": "FT 晶粒级参数原始数据视图 (FT Parameters Dielevel Raw Data Production View)",
    "dwd_ft_parameters_dutlevel_rawdata_prod_v": "FT DUT 级参数原始数据视图 (FT Parameters DUT Level Raw Data Production View)",
    "dws_autoink_rule_wf": "自动墨点规则工作流 (Auto Ink Rule Workflow)",
    "dwd_autoink_wafers_detail_v": "自动墨点晶圆详情视图 (Auto Ink Wafers Detail View)",
    "dwd_abnormal_label": "异常标签 (Abnormal Label)",
    "dwd_fac_material": "工厂物料 (Factory Material)"
}




# 数据描述：
# {data_type_descriptions}

# 数据表名：
# {table_name_map}

df_result = pd.read_excel('data.xlsx')
res_list = []
if not os.path.exists('new_data.xlsx'):
    df = pd.read_excel('data.xlsx')
    df.ffill(inplace=True)
    df.to_excel("new_data.xlsx",index=False)
    df.to_csv("data.csv")
    exit(0)
else:
    df = pd.read_excel('new_data.xlsx')
    
    for index, row in df.iterrows():
        data_type = row.iloc[0]

        summary_or_raw = row.iloc[1]
        
        data_type = row.iloc[2]
        # print(data_type)
        # data_type = row.iloc[3]
        
        # print(data_type)
        table_name = row.iloc[4]
        print(table_name)
        query_scroe = row.iloc[5].replace("时间",'time').replace("产品","product")
        # print(query_scroe)
        
        q = f"""
        背景信息：
        你正在使用一个为半导体行业设计的垂直应用系统，该系统支持通过数据分析，提高良品率。

        你的任务：
        - 请你模拟人工提问，提问的方式为，在某一时段内（如：一个星期，一个月），查询 {data_type_descriptions} 中的一个或多条数据。请考虑半导体客户的问题习惯。
        - 该问题一定是关于{table_name}数据表的中{query_scroe}字段的。
        - 该用中文的用中文，该用英文的用英文。输出的格式为 1. 问题1 \n 2. 问题2 \n  3. 问题3 

        数据描述：
        {data_type_descriptions}

        问题示例：

        查询近一个月
 
#         """

        # 我需的问题是关于 {data_type} 数据类型的 ，查询条件为{query_scroe}中的任意一个,其中查询条件的落脚到要在{query_scroe}中，但是不要明说，要用半导体的客户问题

        # 请根据 {query_scroe}，生成3个人工问题。
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": q},
            ],
            stream=False
        )

        print(response.choices[0].message.content)
        res_list.append(response.choices[0].message.content)
        print(f"------------------------------------------------{table_name}---------------------------------------------------------")

        
# print(res_list)        
df_result['question'] = res_list
df_result.to_excel('question.xlsx')