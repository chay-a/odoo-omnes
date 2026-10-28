import {Component} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export class DeleteButton extends Component{
    static template = "volunteering_hours.DeleteButton";
    static props = {
        deleteURL: { type: String, optional: false },
        volunteeringYear: { type: Number, optional: false },
        volunteeringId: { type: Number, optional: false },
        currentYear: { type: String, optional: false },
    }

    async onDelete(evt) {
        const response = await rpc(`/my/volunteering/delete/${evt.currentTarget.dataset.volunteering_id}`)
        window.location.href = response.redirect_url
    }
}

registry
    .category("public_components")
    .add("volunteering_hours.DeleteButton", DeleteButton);