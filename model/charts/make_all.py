"""Rebuild every figure: .venv/bin/python model/charts/make_all.py"""
import importlib
for m in ("fig1_heatmaps", "fig2_childcare", "fig3_credit", "fig4_retention", "fig5_states", "fig6_valve",
          "fig7_box3_split", "fig8_both_pay", "fig9_ceilings", "fig10_ma_shared_vs_primary", "exhibits"):
    importlib.import_module(m).main()
