import {Component} from "@odoo/owl";
import { registry } from "@web/core/registry";

export class DeleteButton extends Component{
    static template = "volunteering_hours.DeleteButton";
    static props = {
        deleteURL: { type: String, optional: false },
        volunteeringYear: { type: Number, optional: false },
        volunteeringId: { type: Number, optional: false },
        currentYear: { type: String, optional: false },
    }
}

registry
    .category("public_components")
    .add("volunteering_hours.DeleteButton", DeleteButton);