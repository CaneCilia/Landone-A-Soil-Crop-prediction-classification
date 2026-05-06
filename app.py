import os
import cv2
import numpy as np
import gradio as gr
from soil_model import classify_soil, estimate_soil_properties
from recommendation import generate_recommendations

HERE = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(HERE, "docs.md"), "r", encoding="utf-8") as f:
    docs_markdown = f.read()

with open(os.path.join(HERE, "about.md"), "r", encoding="utf-8") as f:
    about_markdown = f.read()


def format_metrics(metrics: dict) -> str:
    return (
        f"Soil Type: {metrics['soil_type']}\n"
        f"Soil Confidence: {metrics['confidence']*100:.0f}%\n"
        f"Texture: {metrics['texture']}\n"
        f"Estimated Moisture: {metrics['moisture']}%\n"
        f"Organic Content Estimate: {metrics['organic_content']}%\n"
        f"pH Approximation: {metrics['ph']}"
    )


def format_recommendations(recommendations: list) -> str:
    if not recommendations:
        return "No crop recommendations available for the provided inputs."
    lines = []
    for item in recommendations:
        lines.append(f"• {item['crop']} — Score: {item['score']}%")
        lines.append(f"  Reason: {item['reason']}")
    return "\n".join(lines)


def analyze_soil(image, humidity, temperature, land_size):
    if image is None:
        return (
            "No image uploaded",
            "Upload a soil image to receive predictions.",
            "",
            "Please add a soil image and adjust the environmental values before analysis."
        )

    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    soil_type, confidence = classify_soil(image)
    properties = estimate_soil_properties(soil_type, humidity, temperature)
    properties.update({"soil_type": soil_type, "confidence": confidence})
    recommendations = generate_recommendations(soil_type, properties, humidity, temperature, land_size)

    explanation = (
        f"The system analyzed soil texture, color distribution, and environmental conditions. "
        f"It detected a {soil_type.lower()} profile with {confidence*100:.0f}% confidence. "
        f"The recommendation list ranks crops by suitability for the predicted soil type, moisture level, and temperature."
    )

    return (
        soil_type,
        format_metrics(properties),
        format_recommendations(recommendations),
        explanation
    )


def build_interface():
    with gr.Blocks(title="Soil Health & Crop Recommendation") as demo:
        gr.Markdown("# Soil Health & Crop Recommendation")
        gr.Markdown("Upload a soil image, enter local environmental values, and receive a crop recommendation report.")

        with gr.Row():
            with gr.Column(scale=1):
                image_input = gr.Image(type="numpy", label="Soil Image")
                humidity = gr.Slider(0, 100, value=55, label="Humidity (%)")
                temperature = gr.Slider(-5, 50, value=24, label="Temperature (°C)")
                land_size = gr.Number(value=1.0, label="Land size (hectares)")
                analyze_button = gr.Button("Analyze Soil")

            with gr.Column(scale=1):
                soil_type_output = gr.Textbox(label="Predicted Soil Type", interactive=False)
                metrics_output = gr.Textbox(label="Soil Metrics", lines=8, interactive=False)
                recommendations_output = gr.Textbox(label="Crop Recommendations", lines=12, interactive=False)
                explanation_output = gr.Textbox(label="Explanation", lines=4, interactive=False)

        analyze_button.click(
            analyze_soil,
            inputs=[image_input, humidity, temperature, land_size],
            outputs=[soil_type_output, metrics_output, recommendations_output, explanation_output]
        )

        with gr.Tabs():
            with gr.TabItem("Documentation"):
                gr.Markdown(docs_markdown)
            with gr.TabItem("About"):
                gr.Markdown(about_markdown)

    return demo


if __name__ == "__main__":
    demo = build_interface()
    demo.launch(server_name="0.0.0.0", server_port=7860)
