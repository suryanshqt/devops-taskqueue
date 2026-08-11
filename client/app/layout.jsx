import "./globals.css";

export const metadata = {
  title: "Task Manager",
  description: "Simple task management for DevOps demo",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
