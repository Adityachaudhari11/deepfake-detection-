export async function detectDeepfake(file) {
  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("https://deepfake-detection-1-bzhv.onrender.com/predict", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    return {
      label: data.label,
      message: `Confidence: ${data.confidence.toFixed(2)}%`,
    };
  } catch (error) {
    return { error: "Failed to connect to backend. Please try again." };
  }
}
