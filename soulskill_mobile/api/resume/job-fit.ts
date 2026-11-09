export const config = { api: { bodyParser: false } };

const MAX_BODY_BYTES = 128 * 1024;

export default async function handler(req, res) {
  res.setHeader("Cache-Control", "no-store");
  res.setHeader("X-Content-Type-Options", "nosniff");

  if (req.method !== "POST") {
    res.setHeader("Allow", "POST");
    return res.status(405).json({ detail: "Method not allowed." });
  }

  const backendUrl = (process.env.SOULSKILL_BACKEND_URL || "").replace(/\/+$/, "");
  const bypass = process.env.SOULSKILL_BACKEND_BYPASS || "";
  if (!backendUrl || !bypass) {
    return res.status(503).json({ detail: "The resume service is not configured yet." });
  }

  const contentType = req.headers["content-type"] || "";
  if (!contentType.toLowerCase().startsWith("application/json")) {
    return res.status(415).json({ detail: "A JSON job-fit request is required." });
  }

  const chunks = [];
  let totalBytes = 0;
  try {
    for await (const chunk of req) {
      const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
      totalBytes += buffer.length;
      if (totalBytes > MAX_BODY_BYTES) {
        return res.status(413).json({ detail: "The job-fit request is too large." });
      }
      chunks.push(buffer);
    }

    const upstream = await fetch(backendUrl + "/api/resume/job-fit", {
      method: "POST",
      headers: {
        "content-type": "application/json",
        "x-vercel-protection-bypass": bypass,
      },
      body: Buffer.concat(chunks),
    });

    const responseBody = Buffer.from(await upstream.arrayBuffer());
    res.status(upstream.status);
    res.setHeader(
      "Content-Type",
      upstream.headers.get("content-type") || "application/json",
    );
    return res.send(responseBody);
  } catch (_) {
    return res.status(502).json({ detail: "The resume service could not be reached. Please try again." });
  }
}
