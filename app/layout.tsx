import './globals.css';
import type { Metadata } from 'next';
export const metadata: Metadata={title:'MediKiosk — AI Clinical Intake',description:'Accessible AI-assisted clinical history intake for Indian hospital OPDs'};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en"><body>{children}</body></html>}
