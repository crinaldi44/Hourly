import React from "react";
import './Button.css'

/**
 * Represents a clickable, touchable interactive UI component.
 * @property label - represents the label to display on the button
 * @property onClickHandler - represents the action taken on click
 * @param props - represents the props
 * @constructor
 */
const Button = (props) => {

    return (
        <button className='btn-container' onClick={props.onClick}>
            {props.label}
        </button>
    );
}

export default Button;