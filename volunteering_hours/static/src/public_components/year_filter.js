import {Component, useState} from "@odoo/owl";
import { registry } from "@web/core/registry";

export class YearFilter extends Component{
    static template = "volunteering_hours.YearFilter";
    static props = {
        selectedYear: { type: String, optional: false },
        years: { type: Array, optional: false },
        default: { type: String, optional: true },
    }

    onYearChange(ev) {
        if ('URLSearchParams' in window) {
            const searchParams = new URLSearchParams(window.location.search);
            if (ev.target.value === this.props.default) {
                searchParams.delete("selected_year");
            } else {
                searchParams.set("selected_year", ev.target.value);
            }
            window.location.search = searchParams.toString();
        }
    }
}

registry
    .category("public_components")
    .add("volunteering_hours.YearFilter", YearFilter);