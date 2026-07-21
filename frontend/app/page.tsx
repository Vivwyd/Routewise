"use client";

import dynamic from "next/dynamic";

const RoutePlanner = dynamic(() => import("@/components/RoutePlanner"), {
  ssr: false,
});

export default function Home() {
  return <RoutePlanner />;
}