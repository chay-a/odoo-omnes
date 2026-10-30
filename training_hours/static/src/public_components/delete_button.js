import {Component} from "@odoo/owl";
import { registry } from "@web/core/registry";
import { rpc } from "@web/core/network/rpc";

export class DeleteButton extends Component{
    static template = "training_hours.DeleteButton";
    static props = {
        deleteURL: { type: String, optional: false },
        trainingId: { type: Number, optional: false }
    }

    async onDelete(evt) {
        const response = await rpc(`${this.props.deleteURL}${evt.currentTarget.dataset.training_id}`)
        window.location.href = response.redirect_url
    }
}

registry
    .category("public_components")
    .add("training_hours.DeleteButton", DeleteButton);