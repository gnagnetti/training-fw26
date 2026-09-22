import { createFileRoute } from "@tanstack/react-router";

const ALLOWED_HOST = "cdn.jooraccess.com";

export const Route = createFileRoute("/api/public/image")({
  server: {
    handlers: {
      GET: async ({ request }) => {
        const source = new URL(request.url).searchParams.get("url");
        if (!source) return new Response("Missing image URL", { status: 400 });

        let imageUrl: URL;
        try {
          imageUrl = new URL(source);
        } catch {
          return new Response("Invalid image URL", { status: 400 });
        }

        if (imageUrl.protocol !== "https:" || imageUrl.hostname !== ALLOWED_HOST) {
          return new Response("Image host not allowed", { status: 403 });
        }

        const response = await fetch(imageUrl, { redirect: "follow" });
        if (!response.ok) return new Response("Image unavailable", { status: 502 });

        const contentType = response.headers.get("content-type") ?? "";
        if (!contentType.startsWith("image/"))
          return new Response("Invalid image response", { status: 502 });

        return new Response(response.body, {
          headers: {
            "Content-Type": contentType,
            "Cache-Control": "public, max-age=86400",
          },
        });
      },
    },
  },
});
